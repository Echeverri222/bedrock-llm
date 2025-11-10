#!/bin/bash

# Quick API Test Script
# Usage: ./test_api.sh [your-api-token]

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"
TOKEN="${1:-your-token-here}"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🧪 API Testing Script                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: Root endpoint (no auth required)
echo -e "${YELLOW}Test 1: Root Endpoint${NC}"
curl -s "$API_URL/" | python3 -m json.tool
echo -e "\n${GREEN}✅ Passed${NC}\n"

# Test 2: Health check (requires auth)
echo -e "${YELLOW}Test 2: Health Check (Authenticated)${NC}"
curl -s -X GET "$API_URL/health" \
     -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo -e "\n${GREEN}✅ Passed${NC}\n"

# Test 3: List files (requires auth)
echo -e "${YELLOW}Test 3: List Files${NC}"
curl -s -X GET "$API_URL/files" \
     -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo -e "\n${GREEN}✅ Passed${NC}\n"

# Test 4: Query data (requires auth)
echo -e "${YELLOW}Test 4: Query Data - Count Studies${NC}"
curl -s -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cuántos estudios hay en total?"}' | python3 -m json.tool
echo -e "\n${GREEN}✅ Passed${NC}\n"

# Test 5: Query data - Most expensive study
echo -e "${YELLOW}Test 5: Query Data - Most Expensive Study${NC}"
curl -s -X POST "$API_URL/api/query" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "What was the most expensive study and how much did it cost?"}' | python3 -m json.tool
echo -e "\n${GREEN}✅ Passed${NC}\n"

# Test 6: Invalid token (should fail with 401)
echo -e "${YELLOW}Test 6: Invalid Token (Should Fail)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/health" \
     -H "Authorization: Bearer invalid-token-123")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" == "401" ]; then
    echo -e "${GREEN}✅ Correctly rejected invalid token (401 Unauthorized)${NC}"
else
    echo -e "${RED}❌ Expected 401, got $HTTP_CODE${NC}"
fi
echo ""

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   ✅ Testing Complete!                                 ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"

