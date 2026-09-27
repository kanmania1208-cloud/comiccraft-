from fpdf import FPDF


def create_pdf(story, filename):

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    pdf.set_font(
        "Arial",
        "B",
        24
    )

    pdf.cell(
        0,
        15,
        "ComicCraft",
        ln=True,
        align="C"
    )

    pdf.set_font(
        "Arial",
        "B",
        14
    )

    pdf.cell(
        0,
        10,
        "AI Comic Story",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font(
        "Arial",
        size=11
    )

    for line in story.split("\n"):

        line = line.strip()

        if not line:
            pdf.ln(4)
            continue

        line = line.replace("**", "")
        line = line.replace("*", "")

        try:

            pdf.multi_cell(
                0,
                7,
                line
            )

        except UnicodeEncodeError:

            clean_line = (
                line
                .encode("latin-1", "replace")
                .decode("latin-1")
            )

            pdf.multi_cell(
                0,
                7,
                clean_line
            )

    pdf.output(filename)

    return filename