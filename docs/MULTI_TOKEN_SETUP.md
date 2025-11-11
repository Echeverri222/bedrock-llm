# 👥 Multi-Token Setup (Per-User Tokens)

Upgrade your API to support multiple tokens with per-user access control.

## Why Multiple Tokens?

### Current Setup (Single Token):
- ❌ Everyone shares one token
- ❌ Can't track individual usage
- ❌ Can't revoke one user's access
- ❌ Security risk if leaked

### Multi-Token Setup:
- ✅ Each user gets their own token
- ✅ Track usage per user
- ✅ Revoke individual access
- ✅ Better security and audit trail

---

## Quick Implementation

### Option 1: Simple Token List (5 minutes)

Update your `.env` file and Railway variables:

```bash
# Instead of single token:
API_TOKEN=6a12a1f2...

# Use comma-separated list:
API_TOKENS=token1_user_admin,token2_user_analyst,token3_user_viewer

# Or with labels:
API_TOKENS=admin:6a12a1f2...,analyst:9b34c5e6...,viewer:2d45f8a1...
```

**Update `api.py`:**

```python
# Load multiple tokens
API_TOKENS = os.getenv("API_TOKENS", "").split(",")
if not API_TOKENS or API_TOKENS == [""]:
    logger.warning("⚠️  No API tokens configured!")
    API_TOKENS = []

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """Verify the Bearer token against list of valid tokens"""
    token = credentials.credentials
    
    # Support both labeled and unlabeled tokens
    valid_tokens = []
    for token_entry in API_TOKENS:
        if ":" in token_entry:
            # Format: "user:token"
            _, token_value = token_entry.split(":", 1)
            valid_tokens.append(token_value)
        else:
            # Format: "token"
            valid_tokens.append(token_entry)
    
    if token not in valid_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Optional: Log which token was used (for audit)
    logger.info(f"Request authenticated with token: {token[:8]}...")
    
    return True
```

**Generate tokens for team:**

```bash
# Admin token
echo "Admin: $(openssl rand -hex 32)"

# Analyst token
echo "Analyst: $(openssl rand -hex 32)"

# Viewer token
echo "Viewer: $(openssl rand -hex 32)"
```

**Railway configuration:**
```bash
API_TOKENS=admin:6a12a1f2250df9edcea50e7b00b30142f353749c1965960770a32ed2e61d3c64,analyst:9b34c5e6a7d8f1e2b3c4a5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6,viewer:2d45f8a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9
```

---

## Option 2: Token Database (30 minutes)

For production with many users, use a database:

### Create Token Management

**Create `src/utils/token_manager.py`:**

```python
"""
Token Management System
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
import json
import os

class TokenManager:
    """Manage API tokens with metadata"""
    
    def __init__(self, tokens_file: str = "tokens.json"):
        self.tokens_file = tokens_file
        self.tokens = self._load_tokens()
    
    def _load_tokens(self) -> Dict:
        """Load tokens from file"""
        if os.path.exists(self.tokens_file):
            with open(self.tokens_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_tokens(self):
        """Save tokens to file"""
        with open(self.tokens_file, 'w') as f:
            json.dump(self.tokens, f, indent=2)
    
    def create_token(self, user_id: str, name: str, expires_days: int = 90) -> str:
        """
        Create a new token for a user
        
        Args:
            user_id: Unique user identifier
            name: Descriptive name (e.g., "John Smith - Analyst")
            expires_days: Token validity in days
            
        Returns:
            The generated token
        """
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        expiry = datetime.now() + timedelta(days=expires_days)
        
        self.tokens[token_hash] = {
            "user_id": user_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "expires_at": expiry.isoformat(),
            "active": True,
            "last_used": None,
            "request_count": 0
        }
        
        self._save_tokens()
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify a token and return user info
        
        Returns:
            User info if valid, None if invalid
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        if token_hash not in self.tokens:
            return None
        
        token_data = self.tokens[token_hash]
        
        # Check if active
        if not token_data["active"]:
            return None
        
        # Check expiry
        if datetime.fromisoformat(token_data["expires_at"]) < datetime.now():
            return None
        
        # Update usage stats
        token_data["last_used"] = datetime.now().isoformat()
        token_data["request_count"] += 1
        self._save_tokens()
        
        return token_data
    
    def revoke_token(self, token: str) -> bool:
        """Revoke a token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        if token_hash in self.tokens:
            self.tokens[token_hash]["active"] = False
            self._save_tokens()
            return True
        return False
    
    def list_tokens(self) -> Dict:
        """List all tokens with metadata (without showing actual tokens)"""
        return {
            hash[:8]: {
                "user": data["name"],
                "created": data["created_at"],
                "expires": data["expires_at"],
                "active": data["active"],
                "requests": data["request_count"]
            }
            for hash, data in self.tokens.items()
        }
```

**Update `api.py` to use TokenManager:**

```python
from utils.token_manager import TokenManager

# Initialize token manager
token_manager = TokenManager()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict:
    """Verify token and return user info"""
    token = credentials.credentials
    
    user_info = token_manager.verify_token(token)
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"Request by: {user_info['name']} (ID: {user_info['user_id']})")
    return user_info

# Update query endpoint to log user
@app.post("/api/query", response_model=QueryResponse, tags=["Query"])
async def query_data(
    request: QueryRequest,
    user_info: Dict = Security(verify_token)  # Now returns user info
):
    """Query with user tracking"""
    try:
        initialize_services()
        
        logger.info(f"Query by {user_info['name']}: {request.question}")
        
        # ... rest of the code
```

**Create admin script to manage tokens:**

Create `manage_tokens.py`:

```python
#!/usr/bin/env python3
"""
Token Management CLI
"""
import sys
from src.utils.token_manager import TokenManager

def main():
    manager = TokenManager()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_tokens.py create <user_id> <name>")
        print("  python manage_tokens.py list")
        print("  python manage_tokens.py revoke <token>")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 4:
            print("Usage: create <user_id> <name>")
            return
        
        user_id = sys.argv[2]
        name = " ".join(sys.argv[3:])
        
        token = manager.create_token(user_id, name)
        print(f"✅ Token created for {name}")
        print(f"Token: {token}")
        print(f"\n⚠️  Save this token securely - it won't be shown again!")
    
    elif command == "list":
        tokens = manager.list_tokens()
        print("\n📋 Active Tokens:\n")
        for hash_prefix, info in tokens.items():
            status = "✅" if info["active"] else "❌"
            print(f"{status} {hash_prefix}... | {info['user']} | Requests: {info['requests']}")
    
    elif command == "revoke":
        if len(sys.argv) < 3:
            print("Usage: revoke <token>")
            return
        
        token = sys.argv[2]
        if manager.revoke_token(token):
            print("✅ Token revoked")
        else:
            print("❌ Token not found")

if __name__ == "__main__":
    main()
```

**Usage:**

```bash
# Create tokens for team
python manage_tokens.py create admin "Admin User"
python manage_tokens.py create analyst1 "John Smith - Analyst"
python manage_tokens.py create analyst2 "Jane Doe - Analyst"

# List all tokens
python manage_tokens.py list

# Revoke a token
python manage_tokens.py revoke abc123def456...
```

---

## Option 3: Full User Management System

For enterprise use, integrate with:

- **Auth0**: Full authentication platform
- **AWS Cognito**: AWS-native auth
- **Supabase Auth**: Open-source alternative
- **Firebase Auth**: Google's auth solution

These provide:
- ✅ User registration/login
- ✅ Password management
- ✅ OAuth (Google, GitHub, etc.)
- ✅ Role-based access control
- ✅ Audit logs

---

## Comparison

| Feature | Single Token | Token List | Token DB | Full Auth |
|---------|-------------|------------|----------|-----------|
| **Setup** | 1 min | 5 min | 30 min | 2-4 hours |
| **Users** | All shared | 5-10 | Unlimited | Unlimited |
| **Tracking** | ❌ | Basic | ✅ Full | ✅ Enterprise |
| **Revoke** | All or none | Individual | Individual | Individual |
| **Audit** | ❌ | ❌ | ✅ | ✅ Full |
| **Cost** | Free | Free | Free | $0-25/mo |

---

## Recommendation

**For your current needs (small team):**
- Use **Option 1: Token List** (5 minutes)
- Create 3-5 tokens for your team
- Label them for easy management

**When you grow (10+ users):**
- Upgrade to **Option 2: Token Database**
- Track usage per user
- Better security and audit trail

**For enterprise:**
- Use **Option 3: Full Auth System**
- Professional user management
- Role-based access control

---

## Security Best Practices

Regardless of which option:

1. **Generate Strong Tokens**
   ```bash
   openssl rand -hex 32  # 64 character hex
   ```

2. **Rotate Regularly**
   - Admin tokens: Every 30 days
   - User tokens: Every 90 days
   - Service tokens: Every 180 days

3. **Track Usage**
   - Monitor request logs
   - Alert on unusual patterns
   - Audit access regularly

4. **Secure Storage**
   - Use password managers
   - Never commit tokens to git
   - Encrypt tokens.json in production

5. **Revoke Immediately**
   - When employee leaves
   - If token is compromised
   - After suspicious activity

---

## Quick Start: Implement Token List Now

Want to upgrade to multiple tokens right now? Run this:

```bash
# Generate 3 tokens
echo "ADMIN_TOKEN=$(openssl rand -hex 32)"
echo "ANALYST_TOKEN=$(openssl rand -hex 32)"
echo "VIEWER_TOKEN=$(openssl rand -hex 32)"
```

Add to Railway variables:
```
API_TOKENS=admin:TOKEN1,analyst:TOKEN2,viewer:TOKEN3
```

Share tokens securely with your team! 🔐

