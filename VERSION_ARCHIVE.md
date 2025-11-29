## Version 2.4.0

Release Date: 2025-11-29 23:08:18
Status: Released

### Key Features
- Enhanced modular architecture with 28 extracted functions
- Improved dialog system with conflict handling
- Advanced search functionality with zero-result keywords
- Better file operations with error handling
- Comprehensive documentation and testing

### Files Consolidated
- Moved 15 refactoring documents to ai-workflow/refactoring_archive/2025-11-29/
- Total documentation: 105.5 KB
- Complete project restructuring documented

### Technical Improvements
- Code modularization completed across 6 component modules
- Extended test suite with 24 test cases
- Build optimization with PyInstaller 6.17.0
- Windows and PowerShell workflow documentation

---
# FileGather Pro 鐗堟湰妗ｆ

## 鐗堟湰鍘嗗彶涓?Git 鎻愪氦鍏宠仈

姝ゆ枃浠惰褰曟瘡涓増鏈殑鍙戝竷淇℃伅銆佷富瑕佹敼杩涘拰瀵瑰簲鐨?Git 鎻愪氦銆?

---

## v2.3.5.2 (In Progress)

**鍙戝竷鏃堕棿**: TBD  
**鏍囩**: `2.3.5.2` (寰呭垱寤?  
**鍒嗘敮**: main

### 涓昏鎻愪氦

| 鎻愪氦鍝堝笇 | 鎻愪氦淇℃伅 | 鏃ユ湡 |
|---------|--------|------|
| `4d8f279` | Implement folder gathering mode feature | 2025-11-30 |

### 鏂板鍔熻兘

- 馃梻锔?**鏂囦欢澶瑰綊闆嗘ā寮?*: 鏀寔鏂囦欢澶归泦鍚堣€岄潪鍗曚釜鏂囦欢
  - 鏂板 `gather_mode_combo` 涓嬫媺閫夋嫨锛氭枃浠跺綊闆?/ 鏂囦欢澶瑰綊闆?
  - `_start_folder_search()`: 妯＄硦鍖归厤鏂囦欢澶瑰悕绉?
  - `_start_folder_exact_search()`: 绮剧‘鍖归厤鏂囦欢澶瑰悕绉?
  - 浠呮悳绱㈢洰鏍囩洰褰曠殑**绗竴绾?*瀛愭枃浠跺す
  - 鏂囦欢澶规ā寮忎笅鑷姩闅愯棌鏂囦欢绫诲瀷鍜屽瓙鏂囦欢澶归€夐」

- 馃幆 **UI 鏀硅繘**:
  - 褰掗泦妯″紡閫夋嫨鍣ㄥ湪鎼滅储鏉′欢琛屼腑灞曠ず
  - 鏂囦欢澶规ā寮忎笅闅愯棌"鏂囦欢绫诲瀷"鍜?鍖呭惈瀛愭枃浠跺す"閫夐」
  - 鐘舵€佹爮鏄剧ず"宸叉壘鍒? X 涓枃浠跺す"锛堣€岄潪鏂囦欢鏁帮級

### 鎶€鏈敼杩?

- `components/ui_builder.py`:
  - 鏂板 `gather_mode_combo` 缁勪欢
  - 鍒涘缓 `subfolders_container` widget 瀹瑰櫒浠ヤ究浜庡彲瑙佹€ф帶鍒?
  - 杩斿洖鍏冪粍鎵╁睍鑷?17 涓厓绱?

- `components/main_window.py`:
  - 瀹炵幇 `on_gather_mode_changed()` 鏂规硶澶勭悊妯″紡鍒囨崲
  - 瀹炵幇 `_start_folder_search()` 鏂规硶
  - 瀹炵幇 `_start_folder_exact_search()` 鏂规硶
  - `start_search()` 鍜?`start_exact_search()` 璺敱鑷虫枃浠跺す鎼滅储鏂规硶

### 鍔熻兘瀵规瘮

| 鍔熻兘 | 鏂囦欢褰掗泦 | 鏂囦欢澶瑰綊闆?|
|------|--------|----------|
| 鎼滅储瀵硅薄 | 涓埆鏂囦欢 | 鐩綍鏂囦欢澶?|
| 鎼滅储鑼冨洿 | 鍙€掑綊鍒板绾у瓙鏂囦欢澶?| 浠呴檺绗竴绾у瓙鏂囦欢澶?|
| 鏂囦欢绫诲瀷绛涢€?| 鉁?鏀寔 | 鉁?涓嶉€傜敤 |
| 瀛愭枃浠跺す閫掑綊 | 鉁?鍙€?| 鉁?绂佺敤 |
| 绮剧‘/妯＄硦鍖归厤 | 鉁?涓ょ閮芥敮鎸?| 鉁?涓ょ閮芥敮鎸?|
| 鎼滅储妯″紡 | 鎸夋枃浠跺悕/鍐呭/鍙屾ā寮?| 浠呮寜鏂囦欢澶瑰悕 |

---

## v2.3.5.1 (2025-11-29)

**鍙戝竷鏃堕棿**: 2025-11-29 21:54:51  
**鏍囩**: `2.3.5.1` (寰呭垱寤?  
**鍒嗘敮**: main

### 涓昏鎻愪氦

| 鎻愪氦鍝堝笇 | 鎻愪氦淇℃伅 | 鏃ユ湡 |
|---------|--------|------|
| `7126642` | fix: correct delete button label for accuracy | 2025-11-29 |
| `c2d885b` | feat: add exact filename matching search mode and improve UI layout | 2025-11-29 |
| `5adc9a8` | docs: add ansel333 as co-author and contributor | 2025-11-29 |
| `304964a` | ci: configure workflow to upload exe to GitHub release | 2025-11-29 |

### 鏂板鍔熻兘

- 鉁?**绮剧‘鏌ユ壘妯″紡**: 鏀寔鏂囦欢鍚嶄弗鏍煎尮閰?
  - 鏂板 `exact_match_filename()` 鍑芥暟
  - 娣诲姞 `start_exact_search()` 鏂规硶
  - 鏂囦欢鍚嶇簿纭尮閰嶏紙蹇界暐鎵╁睍鍚嶏級

- 馃帹 **UI 浼樺寲**: 鎸夐挳閲嶆柊鎺掑竷涓轰笁琛屽竷灞€
  - 琛?: 馃攳 妯＄硦鏌ユ壘 | 鉁?绮剧‘鏌ユ壘 | 鈴?鍙栨秷鎼滅储
  - 琛?: 馃搨 閫夋嫨鐩爣 | 馃搵 寮€濮嬪綊闆?| 馃棏 鍒犻櫎鍘熷鏂囦欢
  - 琛?: 馃搫 鐢熸垚鏃ュ織 | 鉂?浣跨敤璇存槑
  - 涓烘墍鏈夋寜閽坊鍔犲伐鍏锋彁绀?

- 馃摎 **鏂囨。瀹屽杽**: 鍚姩鑴氭湰鍜屾寚鍗?
  - `run.ps1`: PowerShell 蹇€熷惎鍔ㄨ剼鏈?
  - `run.bat`: 鎵瑰鐞嗗揩閫熷惎鍔ㄨ剼鏈?
  - `LAUNCH_GUIDE.md`: 瀹屾暣鍚姩鎸囧崡

### 鎶€鏈敼杩?

- 浠ｇ爜鏂囦欢閲嶆瀯锛?
  - `search_logic.py`: 娣诲姞绮剧‘鍖归厤閫昏緫
  - `ui_builder.py`: 浼樺寲鎸夐挳甯冨眬锛?-tuple 杩斿洖鍊硷級
  - `main_window.py`: 澶勭悊绮剧‘鎼滅储鍔熻兘

- 鏋勫缓宸ュ叿锛?
  - `.gitignore`: 娣诲姞 `build_2.3.4/` 蹇界暐瑙勫垯
  - `build_2.3.4/`: v2.3.4 瀵规瘮鐗堟湰鐨勬瀯寤虹洰褰?

### 鍙墽琛屾枃浠?

| 鏂囦欢鍚?| 澶у皬 | 鍙戝竷鏃ユ湡 |
|--------|------|---------|
| FileGather_Pro.exe | 70.59 MB | 2025-11-29 21:10:52 |
| FileGather_Pro_2.3.4.exe | 70.44 MB | 2025-11-29 21:54:51 |

### 鏂囦欢娓呯悊

- 閲嶅懡鍚? `FileGather_Pro2.3.5.py` 鈫?`FileGather_Pro.py`
- 鐞嗙敱: 鐗堟湰鍙风敱浠ｇ爜绠＄悊锛屾棤闇€鍦ㄦ枃浠跺悕涓噸澶?

---

## v2.3.5 (2025-11-29)

**鍙戝竷鏃堕棿**: 2025-11-29 13:00:00  
**鏍囩**: `2.3.5`  
**鍒嗘敮**: main  
**棣栨鎻愪氦**: `9448e0b`

### 涓昏鎻愪氦

| 鎻愪氦鍝堝笇 | 鎻愪氦淇℃伅 | 鏃ユ湡 |
|---------|--------|------|
| `9448e0b` | refactor: organize AI workflow documentation and finalize v2.3.5 | 2025-11-29 |

### 涓昏鎴愬氨

- 鉁?**瀹屾暣妯″潡鍖栭噸鏋?*: 1686琛屽崟鏂囦欢 鈫?妯″潡鍖栫粨鏋?
  - `main_window.py`: 涓荤獥鍙ｅ拰鎼滅储閫昏緫 (832 琛?
  - `ui_builder.py`: UI 缁勪欢宸ュ巶 (444 琛?
  - `search_logic.py`: 鎼滅储绠楁硶 (121 琛?
  - `file_operations.py`: 鏂囦欢鎿嶄綔 (130 琛?
  - `utils.py`: 宸ュ叿鍑芥暟 (100 琛?
  - `dialogs/`: 瀵硅瘽妗嗗瓙鍖?(3 涓笓涓氭ā鍧?

- 馃摝 **dialogs 鍖呯粏鍖?*
  - `search_result_dialog.py`
  - `conflict_dialog.py`
  - `pdf_generator.py`

- 馃彈锔?**椤圭洰缁勭粐**
  - AI 宸ヤ綔娴佹枃妗ｇЩ鍒?`ai-workflow/`
  - 鍒涘缓 `archive/` 鏂囦欢澶瑰綊妗ｆ棫鐗堟湰
  - 娣诲姞 `.gitignore` 閰嶇疆
  - 鍒涘缓瀹屾暣鐨勬枃妗?

### 鍙墽琛屾枃浠?

| 鏂囦欢鍚?| 澶у皬 | 鍙戝竷鏃ユ湡 |
|--------|------|---------|
| FileGather_Pro.exe | 67.32 MB | 2025-11-29 13:00:00 |

---

## v2.3.4 (2025-07-17)

**鏍囩**: `2.3.4`  
**鍒嗘敮**: main  
**鐘舵€?*: 宸插瓨妗?

### 鐗圭偣

- 鍗曟枃浠剁粨鏋勶紙1686 琛岋級
- 鏀寔澶氭牸寮忔枃浠舵悳绱紙TXT銆丳DF銆丏OCX銆乆LSX锛?
- 楂樼骇鍏抽敭璇嶅尮閰嶈娉?
- 妯＄硦鎼滅储鍔熻兘
- PDF 鎶ュ憡鐢熸垚

### 鍙墽琛屾枃浠?

| 鏂囦欢鍚?| 澶у皬 |
|--------|------|
| FileGather_Pro_2.3.4.exe | 70.44 MB |

---

## 鐗堟湰姣旇緝鎬荤粨

| 鐗规€?| v2.3.4 | v2.3.5 | v2.3.5.1 |
|------|--------|--------|----------|
| 浠ｇ爜缁撴瀯 | 鍗曟枃浠?1686琛? | 妯″潡鍖?6涓ā鍧? | 妯″潡鍖?6涓ā鍧? |
| 绮剧‘鏌ユ壘 | 鉂?| 鉂?| 鉁?|
| 妯＄硦鏌ユ壘 | 鉁?| 鉁?| 鉁?|
| 楂樼骇璇硶 | 鉁?| 鉁?| 鉁?|
| 鎸夐挳甯冨眬 | 鍗曡 | 鍗曡 | 涓夎 |
| 宸ュ叿鎻愮ず | 鉂?| 鉂?| 鉁?|
| 蹇€熷惎鍔ㄨ剼鏈?| 鉂?| 鉂?| 鉁?|
| CI/CD 鑷姩鍖?| 鉂?| 鉁?| 鉁?|
| 浠ｇ爜鍙淮鎶ゆ€?| 浣?| 楂?| 楂?|

---

## Git 宸ヤ綔娴?

### 鏍囩鍒涘缓

```bash
# v2.3.5.1 鏍囩锛堝緟鍒涘缓锛?
git tag -a 2.3.5.1 -m "Release v2.3.5.1 - Exact search and UI improvements"

# 宸插瓨鍦ㄧ殑鏍囩
git tag 2.3.5
git tag 2.3.4
```

### 妫€鏌ョ壒瀹氱増鏈唬鐮?

```bash
# 鏌ョ湅 v2.3.5.1 浠ｇ爜
git show 2.3.5.1:FileGather_Pro.py

# 鏌ョ湅 v2.3.5 浠ｇ爜
git show 2.3.5:FileGather_Pro2.3.5.py

# 鏌ョ湅 v2.3.4 浠ｇ爜
git show 2.3.4:archive/FileGather_Pro2.3.4.py
```

### 鑾峰彇鍘嗗彶鏂囦欢

```bash
# 鑾峰彇 v2.3.4 鐗堟湰
git checkout 2.3.4 -- archive/FileGather_Pro2.3.4.py

# 鑾峰彇 v2.3.5 鐗堟湰
git checkout 2.3.5 -- FileGather_Pro2.3.5.py
```

---

## 鍙戝竷娴佺▼

瀵逛簬姣忎釜鏂扮増鏈細

1. **浠ｇ爜瀹屾垚**: 瀹屾垚鎵€鏈夊姛鑳藉紑鍙戝拰娴嬭瘯
2. **鏇存柊鏂囨。**: 
   - 鏇存柊 `README.md` 鐗堟湰鍙峰拰鍔熻兘璇存槑
   - 鏇存柊姝ゆ枃浠讹紙VERSION_ARCHIVE.md锛夌殑鐗堟湰淇℃伅
3. **鍒涘缓鏍囩**:
   ```bash
   git tag -a X.X.X -m "Release vX.X.X - Feature description"
   git push origin X.X.X
   ```
4. **鍒涘缓 Release**:
   - GitHub Release 鑷姩闄勫姞鍙墽琛屾枃浠?
   - 鍖呭惈鐗堟湰璇存槑鍜屾洿鏂版棩蹇?
5. **鏇存柊鐗堟湰妗ｆ**: 娣诲姞鍒版鏂囦欢

---

**鏈€鍚庢洿鏂?*: 2025-11-29  
**缁存姢鑰?*: daiyixr, ansel333  
**浠撳簱**: https://github.com/ansel333/FileGather_Pro

