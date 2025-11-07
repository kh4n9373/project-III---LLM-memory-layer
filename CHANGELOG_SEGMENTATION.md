# Changelog - Topic Segmentation System

## Version 1.1 - Environment Configuration & Multi-API Support (Current)

### ✨ New Features

#### 1. **Environment File Support (.env)**
- ✅ Added `python-dotenv` dependency
- ✅ Created `env.example` template với full configuration options
- ✅ Auto-load environment variables từ `.env` file
- ✅ Support cho multiple API configurations

#### 2. **Custom Base URL Support**
- ✅ Support `OPENAI_BASE_URL` environment variable
- ✅ Compatible với Gemini API (OpenAI-compatible endpoint)
- ✅ Support cho local models (via LiteLLM, LocalAI, etc.)
- ✅ Auto-detect và print base URL khi chạy

#### 3. **Improved Configuration System**
- ✅ Config hierarchy: `.env` → command line arguments → defaults
- ✅ New environment variables:
  - `OPENAI_API_KEY` - API key (required)
  - `OPENAI_BASE_URL` - Custom base URL (optional)
  - `DEFAULT_MODEL` - Default model name
  - `DEFAULT_TEMPERATURE` - Default temperature
  - `PROCESS_LIMIT` - Default limit for processing
- ✅ All settings có thể override bằng command line flags

#### 4. **Enhanced Limit Configuration**
- ✅ Added `--start` flag để chọn conversation bắt đầu
- ✅ Improved `--limit` logic với better messaging
- ✅ Support range processing: `--start 10 --limit 5` (process 10-14)
- ✅ Show total conversations và range đang xử lý

#### 5. **Better Error Messages**
- ✅ Clearer error messages cho API key issues
- ✅ Helpful hints về .env setup
- ✅ Troubleshooting tips trong error output
- ✅ Configuration summary trước khi chạy

#### 6. **New Documentation**
- ✅ `SETUP_WITH_ENV.md` - Complete guide cho .env setup
- ✅ Gemini API integration instructions
- ✅ Cost comparison tables
- ✅ Multiple configuration examples
- ✅ Comprehensive troubleshooting section

### 🔧 Updated Files

1. **`requirements_segmentation.txt`**
   - Added `python-dotenv>=1.0.0`

2. **`topic_segmentation.py`**
   - Added `get_openai_client()` function với base URL support
   - Load environment variables với `dotenv`
   - Enhanced command line arguments
   - Added configuration printing
   - Improved error handling
   - Added `--start` parameter

3. **`segment_locomo_batch.py`**
   - Load environment variables với `dotenv`
   - Use shared `get_openai_client()` function
   - Updated error messages

4. **`test_segmentation.py`**
   - Load environment variables với `dotenv`
   - Updated error messages với .env hints

5. **New: `env.example`**
   - Complete configuration template
   - Examples cho OpenAI, Gemini, Local models
   - Detailed comments và instructions

6. **New: `SETUP_WITH_ENV.md`**
   - Complete setup guide
   - API-specific configurations
   - Troubleshooting section
   - Cost comparisons
   - Quick start commands

7. **New: `CHANGELOG_SEGMENTATION.md`** (this file)
   - Track all changes và versions

### 📊 Usage Examples

#### Before (v1.0):
```bash
export OPENAI_API_KEY='sk-xxx'
python topic_segmentation.py --limit 2 --model gpt-4o-mini
```

#### After (v1.1):
```bash
# Create .env file
cp env.example .env
# Edit .env với your settings

# Run với .env config
python topic_segmentation.py

# Override khi cần
python topic_segmentation.py --model gemini-1.5-flash --limit 5
```

### 🌟 Supported APIs

| API | Status | Base URL | Models |
|-----|--------|----------|--------|
| OpenAI | ✅ Native | (default) | gpt-4o, gpt-4o-mini, gpt-4-turbo |
| Gemini | ✅ New | `https://generativelanguage.googleapis.com/v1beta/openai/` | gemini-1.5-flash, gemini-1.5-pro |
| Local (LiteLLM) | ✅ New | `http://localhost:8000/v1` | Any local model |
| Azure OpenAI | ✅ New | Custom Azure endpoint | Azure-deployed models |
| Other OpenAI-compatible | ✅ New | Custom URL | Depends on provider |

### 💡 Migration Guide

Nếu bạn đang dùng v1.0:

1. **Update dependencies:**
   ```bash
   pip install -r requirements_segmentation.txt
   ```

2. **Create .env file:**
   ```bash
   cp env.example .env
   # Edit .env với your API key
   ```

3. **Update commands:**
   ```bash
   # Old way still works:
   export OPENAI_API_KEY='sk-xxx'
   python topic_segmentation.py --limit 2
   
   # New way (recommended):
   python topic_segmentation.py  # Reads from .env
   ```

### 🐛 Bug Fixes

- Fixed client initialization timing issues
- Improved error handling cho API failures
- Better validation cho environment variables

---

## Version 1.0 - Initial Release

### Features

- ✅ Core topic segmentation functionality
- ✅ Single-file processing mode
- ✅ Batch processing mode
- ✅ Analysis and validation tools
- ✅ Test script
- ✅ Complete documentation
- ✅ Example outputs
- ✅ OpenAI API integration (default only)

### Files

- `topic_segmentation.py` - Main script
- `segment_locomo_batch.py` - Batch processor
- `analyze_segmentation.py` - Analysis tools
- `test_segmentation.py` - Test script
- `requirements_segmentation.txt` - Dependencies
- `QUICKSTART_SEGMENTATION.md` - Quick start guide
- `TOPIC_SEGMENTATION_README.md` - Full documentation
- `TOPIC_SEGMENTATION_SUMMARY.md` - System overview
- `SEGMENTATION_INDEX.md` - File index
- `README_TOPIC_SEGMENTATION.md` - Main README
- `segmentation_example_output.json` - Example output

---

## Roadmap

### Version 1.2 (Planned)

- [ ] Add caching layer để giảm API calls
- [ ] Support resume từ incomplete runs
- [ ] Add validation rules configuration
- [ ] Parallel processing trong single script
- [ ] Progress saving và checkpoints

### Version 1.3 (Planned)

- [ ] Custom prompt templates
- [ ] Entity linking và normalization
- [ ] Multi-language support
- [ ] Visualization tools
- [ ] Web interface (optional)

### Future Ideas

- [ ] Fine-tuned models cho segmentation
- [ ] Active learning với human feedback
- [ ] Integration với vector databases
- [ ] GraphRAG support
- [ ] Streaming API support

---

## Breaking Changes

### v1.0 → v1.1

**No breaking changes!** 

All v1.0 scripts vẫn hoạt động bình thường. v1.1 chỉ adds new features:
- Old way (environment variables) still works
- New way (.env file) is recommended nhưng optional

---

## Deprecations

None. All v1.0 functionality is preserved.

---

## Contributors

- **hungpv** - Initial implementation
- **AI Assistant** - Development và documentation

---

## License

Use freely for your projects.

---

**Current Version**: 1.1  
**Last Updated**: November 2025  
**Status**: ✅ Stable, Production-ready

