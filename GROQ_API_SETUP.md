# Groq API Setup Guide

## 🚀 **GET A VALID GROQ API KEY**

### **✅ STEP 1: SIGN UP FOR GROQ**
1. Go to: https://groq.com/
2. Click "Sign Up" or "Get Started"
3. Create a free account
4. Verify your email address

### **✅ STEP 2: GET API KEY**
1. Log in to your Groq account
2. Go to: https://console.groq.com/keys
3. Click "Create Key"
4. Give your key a name (e.g., "multimodal-ai-app")
5. Copy the API key - it will start with `gsk_`

### **✅ STEP 3: VALID API KEY FORMAT**
Valid Groq API keys look like:
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Starts with `gsk_`
- 56+ characters long
- Contains letters and numbers

---

## 🔧 **UPDATE API KEY IN RAILWAY**

### **✅ METHOD 1: RAILWAY DASHBOARD**
1. Go to your Railway project
2. Select the backend service
3. Go to "Variables" tab
4. Update `GROQ_API_KEY` with your new key
5. Redeploy the service

### **✅ METHOD 2: RAILWAY CLI**
```bash
# Set new API key
railway variables set GROQ_API_KEY=your_new_gsk_key_here

# Redeploy
railway up
```

### **✅ METHOD 3: ENVIRONMENT FILE**
Update your `.env` file:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

---

## 🧪 **TEST THE API KEY**

### **✅ QUICK TEST**
```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "llama-3.1-8b-instant",
  "messages": [{"role": "user", "content": "Hello"}],
  "max_tokens": 10
}'
```

### **✅ EXPECTED RESPONSE**
```json
{
  "choices": [
    {
      "message": {
        "content": "Hello! How can I help you today?",
        "role": "assistant"
      }
    }
  ]
}
```

---

## 🎯 **AVAILABLE MODELS**

### **✅ FAST MODELS**
- `gemma2-9b-it` - Fast, good for simple queries
- `llama-3.1-8b-instant` - Balanced performance

### **✅ SMART MODELS**
- `llama3-groq-70b-8192-tool-use-preview` - Most capable

---

## 📋 **TROUBLESHOOTING**

### **❌ COMMON ISSUES**
1. **401 Unauthorized** → API key is invalid
2. **403 Forbidden** → API key permissions issue
3. **Rate Limited** → Too many requests, wait and retry
4. **Invalid Model** → Check model name spelling

### **✅ SOLUTIONS**
1. **Generate new API key** from Groq console
2. **Check key permissions** - ensure chat completions allowed
3. **Verify model names** - use exact names from documentation
4. **Check quota** - Free tier has limits

---

## 🚀 **AFTER UPDATING**

### **✅ TEST YOUR APPLICATION**
1. Update API key in Railway
2. Wait for redeployment (2-3 minutes)
3. Test chat functionality
4. Check backend logs for errors

### **✅ VERIFY IT'S WORKING**
- Chat should respond intelligently
- No more "trouble connecting" messages
- File uploads should work with AI analysis

---

## 📞 **SUPPORT**

### **✅ GROQ RESOURCES**
- Documentation: https://groq.com/docs/
- API Reference: https://console.groq.com/docs
- Support: support@groq.com

### **✅ GET HELP**
If you need help:
1. Check Groq API status: https://status.groq.com/
2. Verify your account is active
3. Generate a fresh API key
4. Contact Groq support if needed

---

**🎉 Once you update the API key, your chat application will work perfectly!**
