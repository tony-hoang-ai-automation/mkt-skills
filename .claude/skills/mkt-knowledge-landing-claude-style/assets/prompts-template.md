# Image prompts — {{TITLE}}

Tổng cộng **{{N}}** ảnh cần tạo cho landing page này.

## Cách dùng

1. Mở từng prompt bên dưới, copy toàn bộ phần trong `~~~` block.
2. Paste vào AI33 ([ai33.pro](https://ai33.pro)) — chọn model **Nano Banana Pro** (`gemini-3.1-flash-image-preview`), aspect **16:9**, resolution **2K**.
3. Tải ảnh về, đặt tên đúng số (`1.png`, `2.png`, ...) và đặt vào folder này.
4. Mở lại `{{SLUG}}.html` (hoặc refresh) — HTML sẽ tự nhận ảnh, placeholder biến mất.

## Mẹo gen

- **Prompt length**: AI33 đôi khi trả `temporary_model_error` với prompt > 2000 chars. Nếu fail, giảm bớt phần "annotation labels" hoặc "decorative elements" rồi retry.
- **Text rendering**: Nano Banana Pro render text tiếng Việt có dấu khá tốt nhưng có thể sai 1-2 ký tự. Nếu sai, edit prompt highlight rõ chữ cần render rồi gen lại.
- **Aspect**: AI33 KHÔNG hỗ trợ 16:10. Dùng 16:9 (1344×768) — đó cũng là aspect HTML đã set.
- **Style consistency**: tất cả prompt cùng dùng "Editorial infographic in Claude AI signature style, warm cream background #F0EEE6, hand-drawn editorial line art, NOT vintage NOT parchment" — giữ nhất quán giữa các ảnh.

## Auto-gen toàn bộ (optional)

Nếu muốn gen tự động thay vì paste tay:

```bash
cd {{OUTPUT_FOLDER_PATH}}
# Lặp qua từng prompt, ví dụ ảnh 1:
python3 ~/Documents/GitHub/hoang_brain/.claude/skills/image-post-creator/scripts/generate.py \
  "$(< /tmp/prompt-1.txt)" \
  -o ./1.png -ar 16:9 -p ai33 --size 2K -v
```

(Yêu cầu `AI33_KEY` trong `.env`. Xem `mkt-broll-image` skill để biết chi tiết.)

---

## 1.png — {{IMAGE_1_TITLE}}

**Concept**: {{IMAGE_1_METAPHOR}}
**Aspect**: 16:9 · **Resolution**: 2K · **Provider gợi ý**: AI33 (Nano Banana Pro)

~~~
{{FULL_PROMPT_1 — Claude AI editorial style, hand-drawn cream paper, Vietnamese text inside, brand colors specified}}
~~~

---

## 2.png — {{IMAGE_2_TITLE}}

**Concept**: {{IMAGE_2_METAPHOR}}
**Aspect**: 16:9 · **Resolution**: 2K · **Provider gợi ý**: AI33 (Nano Banana Pro)

~~~
{{FULL_PROMPT_2}}
~~~

---

<!-- Repeat cho từng ảnh ... -->

## Checklist trước khi gen

Cho mỗi prompt, đảm bảo:
- [ ] Specify "warm cream background (#F0EEE6)"
- [ ] Specify "hand-drawn editorial line art, NOT parchment, NOT vintage"
- [ ] Vietnamese text với dấu đầy đủ trong các label
- [ ] Brand names giữ tiếng Anh (CLAUDE, DEEPSEEK, OPENAI, …)
- [ ] Visual thinking metaphor cụ thể (heo đất / két sắt / ống nước / …)
- [ ] Brand color hex (#DA7756, #4D6BFE, …)
- [ ] Prompt length < 2000 chars (đếm bằng `wc -c`)
