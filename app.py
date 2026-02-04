import streamlit as st
import json
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("📦 PO Category Classifier")
st.caption("Classify a purchase order description into its category.")

with st.sidebar:
    st.header("Inputs")
    supplier = st.text_input("Supplier (optional)", placeholder="e.g. Acme Medical Supplies")
    st.markdown("---")
    st.markdown("Tip: include brand/model numbers for better accuracy.")

po_description = st.text_area(
    "PO Description",
    height=140,
    placeholder="e.g. 50 boxes of nitrile gloves, size M",
)

classify_clicked = st.button("Classify", type="primary")

result_container = st.container()

if classify_clicked:
    cleaned_description = po_description.strip()
    cleaned_supplier = supplier.strip()

    if not cleaned_description:
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(cleaned_description, cleaned_supplier or None)

        with result_container:
            st.subheader("Result")
            if isinstance(result, dict):
                st.json(result)
                st.text_area("Copy JSON", value=json.dumps(result, indent=2), height=160)
            else:
                try:
                    parsed = json.loads(result)
                    st.json(parsed)
                    st.text_area("Copy JSON", value=json.dumps(parsed, indent=2), height=160)
                except Exception:
                    st.error("Invalid model response")
                    st.text(result)
