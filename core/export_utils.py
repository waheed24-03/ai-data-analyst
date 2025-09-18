import streamlit as st
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def export_csv(df, label="Download CSV", file_name="dataset_export.csv"):
    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=file_name,
        mime="text/csv",
        help="Download your dataset as a CSV file."
    )

def export_plots(figs):
    import matplotlib.pyplot as plt

    if figs:
        for i, fig in enumerate(figs):
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            st.download_button(
                label=f"Download Plot {i+1} as PNG",
                data=buf,
                file_name=f"plot_{i+1}.png",
                mime="image/png"
            )

def export_pdf(df, summary_text, figs=None, file_name="dataset_report.pdf"):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer)
    styles = getSampleStyleSheet()
    elements = []

    # Add AI Summary
    elements.append(Paragraph("AI Dataset Summary", styles['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(summary_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add plots if any
    if figs:
        for fig in figs:
            img_buf = io.BytesIO()
            fig.savefig(img_buf, format='png')
            img_buf.seek(0)
            elements.append(Image(img_buf))
            elements.append(Spacer(1, 12))

    doc.build(elements)
    pdf_buffer.seek(0)

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=file_name,
        mime="application/pdf"
    )
