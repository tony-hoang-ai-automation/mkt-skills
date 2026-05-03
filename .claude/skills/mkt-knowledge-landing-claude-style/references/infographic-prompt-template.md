# Infographic prompt template — Claude AI editorial signature style

Mỗi `<p id="pN">` (ẩn `sr-only`) chứa 1 prompt theo template này. User click "Copy prompt — IMAGE #N" sẽ lấy được full prompt để paste vào Nano Banana Pro / AI33 / Midjourney.

## Tại sao style này

User đã reject:
- ❌ Vintage parchment / Da Vinci technical drawing (giấy cũ, mép rách)
- ❌ Flat-vector dark navy infographic

User đã accept:
- ✅ Hand-drawn editorial trên warm cream `#F0EEE6`, kiểu spot illustration trên claude.ai marketing pages — clean modern hand-drawn, NOT vintage

Đây là design language Claude AI dùng cho marketing material: warm cream paper, line art có confidence stroke, subtle color fills, intelligent friendly feel. Tạo contrast đẹp với body dark navy của landing page (như embedded "artifact").

## Quy tắc cứng (luôn áp dụng)

| Rule | Spec |
|---|---|
| Background | warm cream `#F0EEE6` — modern matte cream like Claude AI marketing pages, **NOT** parchment, **NOT** vintage, **NOT** aged texture |
| Illustration | hand-drawn editorial line art with subtle warm color fills — confident strokes, modern, polished, like New Yorker spot illustration |
| Visual thinking | mỗi ảnh phải có ẩn dụ trực quan dễ hiểu (xem section "Visual thinking metaphors" bên dưới) |
| Text language | TẤT CẢ chữ trong ảnh tiếng Việt có dấu đầy đủ — chỉ giữ tiếng Anh cho exception |
| Exception language | brand names (CLAUDE, DEEPSEEK, ANTHROPIC, OPENAI, MIT, GPT…), tech terms (TERMINAL, PROXY, API, CLI, SDK, MoE, RAG…), inline code (`$ claude`, `:8082`, `npm…`), math/currency symbols ($, %, ×, ₫, →) |
| Aspect | 16:10 (default), 16:9 cho diagram dài, 1:1 cho icon-style |
| Typography | bold modern serif-sans hybrid (Tiempos Headline / Inter Display feel) cho title, neat sans-serif cho annotation, monospace cho technical labels |
| Palette | cream bg + dark slate text + Claude orange `#DA7756` + brand color tương ứng + accent (green `#3FCF8E` cho saving / amber `#F4B860` cho highlight) |
| File name | `1.png`, `2.png`, `3.png`... (theo số thứ tự xuất hiện trong page) |

## Visual thinking metaphors (gợi ý theo concept)

| Concept | Ẩn dụ |
|---|---|
| **Cost / saving** | Heo đất vỡ (đắt) ↔ két sắt nhỏ gọn (rẻ); cốc đầy tràn ↔ ly đong nhỏ |
| **Speed / latency** | Ốc sên ↔ tên lửa; đồng hồ cát đầy ↔ vơi |
| **Architecture / data flow** | Ống nước (pipe) nối các block, mũi tên chỉ hướng |
| **Comparison** | 2 màn hình terminal / 2 cột scale với chip Yes/Yes |
| **Workflow / steps** | Bậc cầu thang, mũi tên cong nối, gear quay nối tiếp |
| **Learning / progression** | Bậc thang cao dần, hành trình map có pin ghim |
| **Open weight / open source** | Lock mở, két không nắp, ngôi nhà cửa mở |
| **Privacy / local** | Két khoá kín, lưới rào, server cá nhân vs cloud |
| **Composition / mix** | Cocktail nhiều layer, lego ghép, palette pha màu |
| **Choice / decision** | Ngã ba đường, cân nghiêng, mũi tên rẽ |

Khi viết prompt, **chọn 1 metaphor** rồi mô tả layout cụ thể — đừng để model AI tự chế.

## Skeleton prompt (fork & fill)

```
Editorial infographic in Claude AI signature style, {{ASPECT}} aspect ratio. Warm cream background (#F0EEE6) with very subtle paper grain — modern matte cream like Claude AI's marketing pages, NOT parchment, NOT vintage, NOT aged texture. Hand-drawn but clean and confident line illustrations with subtle warm color fills, like a thoughtful New Yorker spot illustration. Generous whitespace, considered composition, friendly intelligent feel.

ALL on-image text in VIETNAMESE WITH FULL DIACRITICS — only brand names ({{BRAND_LIST}}) and {{TECH_OR_SYMBOLS}} stay in English.

TYPOGRAPHY:
• Title in bold modern serif-sans hybrid (Tiempos Headline / Inter Display feel), dark slate text: "{{TITLE_VI}}".
• Subtitle below in lighter weight grey: "{{SUBTITLE_VI}}".
• Annotation labels in neat sans-serif, dark slate ink with handwritten warmth.

{{LAYOUT_DESCRIPTION — describe layout block by block, color accents per block, visual metaphor used, exact Vietnamese text in each label}}

{{DECORATIVE_ELEMENTS — small floating annotation tags with curved hand-drawn connector lines, optional doodle icons (gear, lightning bolt, dollar with strikethrough)}}

Visual style: hand-drawn editorial line illustration in Claude AI marketing aesthetic — confident strokes on warm cream paper, modern minimal feel, NOT parchment, NOT vintage, NOT photorealistic. Palette: cream background (#F0EEE6), dark slate text, {{BRAND_1_NAME}} {{BRAND_1_HEX}}, {{BRAND_2_NAME}} {{BRAND_2_HEX}}, accent {{ACCENT_USE_CASE}} {{ACCENT_HEX}}. Warm, intelligent, considered.
```

## Đầy đủ — ví dụ đã rendered

Xem `assets/examples/deepseek-v4-claude-code.html` để thấy 2 prompt hoàn chỉnh (Image #1 = "PHÉP TÍNH" cost comparison, Image #2 = "HAI TERMINAL" diagram).

### Mini-example — "PHÉP TÍNH"

```
Editorial infographic in Claude AI signature style, 16:10 aspect ratio. Warm cream background (#F0EEE6)…

ALL on-image text in VIETNAMESE WITH FULL DIACRITICS — only brand names (CLAUDE OPUS, DEEPSEEK V4, MIT) and currency/math symbols ($, %, ×, ₫) stay in English.

TYPOGRAPHY:
• Title in bold modern serif-sans hybrid: "PHÉP TÍNH — Cùng một workflow, hai mức giá".
• Subtitle: "Một phiên coding 4 tiếng, tính bằng tiền thật".

LEFT BLOCK (Claude side, accent CLAUDE ORANGE #DA7756):
• Small pill at top: "CLAUDE OPUS" — orange fill.
• Hand-drawn cracked piggy bank illustration: pinkish-orange fill with confident black outline, exaggerated cracks, golden coins ($, ₫) tumbling out. Visual-thinking metaphor: "đốt tiền".
• Big dark slate digits: "$62,50" + caption "/ phiên 4 tiếng".
• 3 hand-drawn annotation tags: "Đắt nhất phân khúc", "Mỗi phiên ≈ một bữa nhà hàng", "Hoá đơn cuối tháng phồng to".

CENTER:
• Big bold orange chevron arrow with "×3000" inside.
• Above: green hand-drawn pill "TIẾT KIỆM 99,97%".
• Below: caption "Cùng tác vụ — chỉ đổi backend model".

RIGHT BLOCK (DeepSeek side, accent DEEPSEEK BLUE #4D6BFE):
• Small pill: "DEEPSEEK V4" — blue fill.
• Hand-drawn small treasure chest, blue-grey fill with brass corners, intact, ONE single gold coin on top. Beside it a tiny minimal blue whale icon.
• Big digits: "$0,02" + "/ phiên 4 tiếng".
• 3 tags: "Rẻ tới mức làm tròn về 0", "Open-weight, MIT license", "Chạy local cũng được".

BOTTOM footnote: "* Ước tính trên 1,5 triệu token input + 300 nghìn token output mỗi phiên".

Visual style: hand-drawn editorial line illustration, NOT parchment, NOT vintage. Palette: cream #F0EEE6, dark slate text, Claude orange #DA7756, DeepSeek blue #4D6BFE, accent green #3FCF8E for savings badge, gold for coins.
```

## Bad prompts — tránh các pattern này

❌ "vintage parchment, aged paper, Da Vinci style" → user đã reject
❌ "flat-vector dark navy infographic" → user đã reject
❌ "photorealistic 3D render" → không match Claude aesthetic
❌ Bỏ qua phần "ALL Vietnamese" → ảnh ra tiếng Anh hết
❌ Mô tả layout chung chung "infographic showing X vs Y" → AI sẽ chế random; phải mô tả block-by-block
❌ Để brand color vague "blue and orange" → phải specify hex `#DA7756` và `#4D6BFE`
❌ Quên specify visual thinking metaphor → ảnh ra abstract

## Workflow viết prompt

1. **Đọc context** — section nào? concept gì cần minh hoạ?
2. **Chọn metaphor** — tra bảng "Visual thinking metaphors" hoặc tự nghĩ — phải là vật thể đời thường ai cũng nhận ra.
3. **Plan layout** — 2 cột? 3 layer? center + radiating? mô tả từng block.
4. **List Vietnamese labels** — heading, subtitle, annotation tags (3-5 tag/block) — viết sẵn từng câu chứ đừng để AI tự sinh.
5. **Spec màu** — brand hex + accent hex.
6. **Fork skeleton prompt** trên, paste content vào, save vào `<p id="pN" class="sr-only">` trong HTML.
