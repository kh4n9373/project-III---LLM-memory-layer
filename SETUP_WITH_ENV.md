# 🔧 Setup với .env và Gemini

Hướng dẫn setup để sử dụng với file `.env` và các API khác nhau (OpenAI, Gemini, etc.)

---

## 📋 Bước 1: Install dependencies

```bash
pip install -r requirements_segmentation.txt
```

Dependencies bao gồm:
- `openai` - OpenAI client library
- `tqdm` - Progress bars
- `python-dotenv` - Load environment variables từ .env

---

## 📋 Bước 2: Tạo file .env

### Option A: Copy từ template

```bash
cp env.example .env
```

### Option B: Tạo file mới

Tạo file `.env` trong thư mục `memory_data/`:

```bash
touch .env
```

---

## 🔑 Bước 3: Cấu hình API

Mở file `.env` và paste cấu hình của bạn:

### 🟢 Cho OpenAI API

```env
# OpenAI GPT-4o-mini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.3
PROCESS_LIMIT=
```

### 🔵 Cho Gemini API (OpenAI-compatible)

```env
# Gemini via OpenAI-compatible endpoint
OPENAI_API_KEY=your-gemini-api-key-here
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
DEFAULT_MODEL=gemini-1.5-flash
DEFAULT_TEMPERATURE=0.3
PROCESS_LIMIT=2
```

**Lưu ý**: 
- Gemini API key lấy từ: https://aistudio.google.com/app/apikey
- Model names: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash-exp`

### 🟣 Cho Local Models (via LiteLLM/LocalAI)

```env
# Local model via LiteLLM
OPENAI_API_KEY=dummy
OPENAI_BASE_URL=http://localhost:8000/v1
DEFAULT_MODEL=local-model-name
DEFAULT_TEMPERATURE=0.3
PROCESS_LIMIT=
```

---

## 🎯 Bước 4: Cấu hình tham số (Optional)

### DEFAULT_MODEL
Model sẽ được dùng mặc định. Có thể override với `--model`.

**OpenAI models:**
- `gpt-4o-mini` - Nhanh, rẻ, quality tốt
- `gpt-4o` - Balanced
- `gpt-4-turbo` - Quality cao nhất
- `gpt-3.5-turbo` - Rẻ nhất

**Gemini models:**
- `gemini-1.5-flash` - Nhanh, rẻ (khuyên dùng)
- `gemini-1.5-pro` - Quality cao hơn
- `gemini-2.0-flash-exp` - Experimental, mới nhất

### DEFAULT_TEMPERATURE
Giá trị từ 0.0 đến 1.0:
- `0.0-0.3` - Consistent, deterministic (khuyên dùng cho segmentation)
- `0.3-0.7` - Balanced
- `0.7-1.0` - Creative, varied

### PROCESS_LIMIT
Giới hạn số conversations xử lý:
- Để trống = xử lý tất cả
- `2` = chỉ xử lý 2 conversations đầu (tốt cho testing)
- `10` = xử lý 10 conversations đầu

---

## ✅ Bước 5: Test setup

```bash
python test_segmentation.py
```

Nếu thấy output giống này là thành công:

```
======================================================================
TOPIC SEGMENTATION TEST
======================================================================

Testing dialogue formatting...

======================================================================
FORMATTED DIALOGUE:
======================================================================
[Turn 1] Caroline: Hey Mel! Good to see you!
[Turn 2] Melanie: Hey Caroline! What's up?
...
======================================================================
✅ Formatting test passed!

Testing segmentation with LLM...
This will make an API call to OpenAI.

======================================================================
SEGMENTATION RESULTS:
======================================================================

📍 Segment 1: LGBTQ support group experience
   ID: seg_1
   Turns: [1, 2, 3, 4, 5]
   ...
```

---

## 🚀 Bước 6: Chạy segmentation

### Test với 2 conversations trước

```bash
python topic_segmentation.py --limit 2
```

Hoặc nếu đã set `PROCESS_LIMIT=2` trong `.env`:

```bash
python topic_segmentation.py
```

### Chạy với range cụ thể

```bash
# Conversations 0-4 (5 conversations)
python topic_segmentation.py --start 0 --limit 5

# Conversations 5-9 (5 conversations)
python topic_segmentation.py --start 5 --limit 5
```

### Override model từ command line

```bash
# Dùng model khác thay vì DEFAULT_MODEL
python topic_segmentation.py --model gemini-1.5-pro --limit 2
```

### Xem configuration trước khi chạy

Khi chạy script, bạn sẽ thấy configuration summary:

```
======================================================================
CONFIGURATION
======================================================================
Model: gemini-1.5-flash
Temperature: 0.3
Start index: 0
Limit: 2
Input: ./processed_data/locomo_processed_data.json
Output: ./processed_data/locomo_segmented_data.json
Base URL: https://generativelanguage.googleapis.com/v1beta/openai/
======================================================================
```

---

## 📊 Ví dụ cấu hình cho datasets lớn

### Cấu hình 1: Test mode (nhanh, rẻ)

```env
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
DEFAULT_MODEL=gemini-1.5-flash
DEFAULT_TEMPERATURE=0.3
PROCESS_LIMIT=2
```

```bash
python topic_segmentation.py
# → Chỉ xử lý 2 conversations với Gemini Flash
```

### Cấu hình 2: Production mode (quality cao)

```env
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_BASE_URL=
DEFAULT_MODEL=gpt-4o
DEFAULT_TEMPERATURE=0.3
PROCESS_LIMIT=
```

```bash
python topic_segmentation.py
# → Xử lý tất cả với GPT-4o
```

### Cấu hình 3: Batch processing

```env
OPENAI_API_KEY=your-gemini-key
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
DEFAULT_MODEL=gemini-1.5-flash
DEFAULT_TEMPERATURE=0.3
PROCESS_LIMIT=
```

```bash
# Xử lý theo batch
python segment_locomo_batch.py process --start 0 --end 5
python segment_locomo_batch.py process --start 5 --end 10

# Merge kết quả
python segment_locomo_batch.py merge
```

---

## 🔍 Troubleshooting

### ❌ Error: "OPENAI_API_KEY not found"

**Nguyên nhân**: File `.env` chưa được tạo hoặc sai vị trí

**Giải pháp**:
```bash
# Kiểm tra file .env có tồn tại không
ls -la .env

# Nếu không có, copy từ template
cp env.example .env

# Edit file .env
nano .env
# hoặc
vim .env
# hoặc mở bằng editor yêu thích
```

### ❌ Error: "Invalid API key"

**Nguyên nhân**: API key sai hoặc hết hạn

**Giải pháp**:
- **OpenAI**: Kiểm tra tại https://platform.openai.com/api-keys
- **Gemini**: Kiểm tra tại https://aistudio.google.com/app/apikey

### ❌ Error: "Model not found"

**Nguyên nhân**: Model name không đúng với API

**Giải pháp**:
- **Với Gemini base URL**: Dùng `gemini-1.5-flash`, `gemini-1.5-pro`, etc.
- **Với OpenAI**: Dùng `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`, etc.

### ❌ Error: "Connection error"

**Nguyên nhân**: Base URL không đúng hoặc mạng không kết nối được

**Giải pháp**:
```bash
# Test connection với curl
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://generativelanguage.googleapis.com/v1beta/openai/models

# Kiểm tra base URL trong .env
cat .env | grep BASE_URL
```

### ⚠️ Warning: Rate limit

**Giải pháp**:
```bash
# Giảm số lượng xử lý
python topic_segmentation.py --limit 1

# Hoặc dùng batch mode với retry
python segment_locomo_batch.py process --retry-delay 2.0
```

---

## 💰 So sánh chi phí

Ước tính cho Locomo dataset (~10 conversations, ~1000 messages):

| API | Model | Cost/1M tokens | Estimated Total | Speed |
|-----|-------|----------------|-----------------|-------|
| Gemini | gemini-1.5-flash | $0.075 | **$0.10-0.30** | ⚡⚡⚡ |
| Gemini | gemini-1.5-pro | $1.25 | $1.50-4.00 | ⚡⚡ |
| OpenAI | gpt-4o-mini | $0.15 | $0.50-2.00 | ⚡⚡⚡ |
| OpenAI | gpt-4o | $2.50 | $5.00-15.00 | ⚡⚡ |
| OpenAI | gpt-4-turbo | $10.00 | $20.00-50.00 | ⚡ |

**💡 Khuyên dùng**: Gemini Flash hoặc GPT-4o-mini cho cost/performance tốt nhất

---

## 📝 Template .env đầy đủ

```env
# =============================================================================
# TOPIC SEGMENTATION CONFIGURATION
# =============================================================================

# API Key (REQUIRED)
# - For OpenAI: Get from https://platform.openai.com/api-keys
# - For Gemini: Get from https://aistudio.google.com/app/apikey
OPENAI_API_KEY=your-api-key-here

# Base URL (OPTIONAL)
# - Leave empty for OpenAI
# - For Gemini: https://generativelanguage.googleapis.com/v1beta/openai/
# - For local: http://localhost:8000/v1
OPENAI_BASE_URL=

# Model (OPTIONAL - default: gpt-4o-mini)
# OpenAI: gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo
# Gemini: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash-exp
DEFAULT_MODEL=gpt-4o-mini

# Temperature (OPTIONAL - default: 0.3)
# Range: 0.0 (deterministic) to 1.0 (creative)
# Recommended: 0.2-0.4 for segmentation
DEFAULT_TEMPERATURE=0.3

# Process Limit (OPTIONAL - default: process all)
# Set a number to limit conversations processed
# Useful for testing or large datasets
# Examples: 2 (test), 10 (small batch), empty (all)
PROCESS_LIMIT=

# =============================================================================
# EXAMPLES
# =============================================================================

# Example 1: OpenAI GPT-4o-mini (recommended for production)
# OPENAI_API_KEY=sk-proj-xxxxx
# OPENAI_BASE_URL=
# DEFAULT_MODEL=gpt-4o-mini
# PROCESS_LIMIT=

# Example 2: Gemini Flash (cheap & fast, good for testing)
# OPENAI_API_KEY=your-gemini-key
# OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
# DEFAULT_MODEL=gemini-1.5-flash
# PROCESS_LIMIT=2

# Example 3: Local model via LiteLLM
# OPENAI_API_KEY=dummy
# OPENAI_BASE_URL=http://localhost:8000/v1
# DEFAULT_MODEL=llama-3-70b
# PROCESS_LIMIT=
```

---

## ✅ Checklist

Sau khi setup xong, check list này:

- [ ] Đã install `requirements_segmentation.txt`
- [ ] Đã tạo file `.env` từ `env.example`
- [ ] Đã paste API key vào `.env`
- [ ] Đã set `OPENAI_BASE_URL` (nếu dùng Gemini hoặc custom API)
- [ ] Đã set `DEFAULT_MODEL` phù hợp với API
- [ ] Đã set `PROCESS_LIMIT` cho testing
- [ ] Đã chạy `python test_segmentation.py` thành công
- [ ] Đã test với `--limit 2` thành công

---

## 🎯 Quick Start Commands

```bash
# 1. Setup
pip install -r requirements_segmentation.txt
cp env.example .env
# → Edit .env với API key và settings của bạn

# 2. Test
python test_segmentation.py

# 3. Run với limit
python topic_segmentation.py --limit 2

# 4. Validate
python analyze_segmentation.py --validate

# 5. Full run (nếu muốn)
python topic_segmentation.py
```

---

**Xong! Bạn đã sẵn sàng để chạy topic segmentation với .env config** 🚀

Nếu gặp vấn đề, check phần Troubleshooting ở trên hoặc chạy `python test_segmentation.py` để debug.

