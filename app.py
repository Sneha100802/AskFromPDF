import streamlit as st
import fitz  # PyMuPDF
import os
import json
from PIL import Image
from io import BytesIO

# Create folders
OUTPUT_DIR = "extracted"
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.title("📘 AskFromPDF – Educational PDF Analyzer")

uploaded_file = st.file_uploader("📤 Upload your educational PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Uploaded! Starting processing...")

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    doc = fitz.open("temp.pdf")
    all_questions = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text().strip()
        images = page.get_images(full=True)

        # Track question + option images
        question_img_path = ""
        option_img_paths = []

        for idx, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            # Heuristic: Assume first image = question, rest = options
            if idx == 0:
                img_name = f"page{page_num+1}_question.{ext}"
                question_img_path = os.path.join(OUTPUT_DIR, img_name)
            else:
                img_name = f"page{page_num+1}_option{idx}.{ext}"
                option_img_path = os.path.join(OUTPUT_DIR, img_name)
                option_img_paths.append(option_img_path)

            # Save image
            with open(os.path.join(OUTPUT_DIR, img_name), "wb") as img_file:
                img_file.write(image_bytes)

        if question_img_path:  # Only add if image exists
            all_questions.append({
                "page": page_num + 1,
                "question": text if text else "Image-based question",
                "image": question_img_path,
                "option_images": option_img_paths
            })

    # Save final structured JSON
    with open("final_output.json", "w", encoding="utf-8") as json_file:
        json.dump(all_questions, json_file, indent=4)

    st.success("✅ Extraction Complete!")
    st.download_button("📥 Download final_output.json", data=json.dumps(all_questions, indent=4), file_name="final_output.json")

    # Preview
    st.subheader("📄 Preview")
    for q in all_questions:
        st.markdown(f"### Page {q['page']}")
        st.markdown(f"**📝 Question Text:** {q['question']}")
        st.image(q['image'], caption="Question Image", width=300)
        st.markdown("**🖼 Option Images:**")
        for opt_img in q['option_images']:
            st.image(opt_img, width=200)
    st.success("✅ All questions and images processed successfully!")