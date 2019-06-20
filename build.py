import pathlib
import sh
import typing


def build_drawio_image(in_path: pathlib.Path, out_path: pathlib.Path, size: str = "1500x2000"):
    sh.node("./drawio-batch/drawio-batch.js", "--bounds", size, in_path, out_path)


def build_pandoc_pdf(out_doc: pathlib.Path, docs_list: typing.List[pathlib.Path], template_file: pathlib.Path):
    sh.pandoc(
        "--to", "latex",
        "--variable", "mainfont:Palatino",
        "--output", out_doc,
        *docs_list)


def main():
    concept_maps_path = pathlib.Path("./concept-maps")
    compiled_path = pathlib.Path("./_build")
    compiled_path.mkdir(exist_ok=True)
    for cmap in concept_maps_path.glob("*.drawio"):
        out_path = compiled_path / cmap.name.replace(".drawio", ".png")
        build_drawio_image(cmap, out_path)

    template_file = pathlib.Path("./templates/main.template.tex")
    out_doc = compiled_path / "doc.pdf"
    docs_list = sorted([x.absolute() for x in pathlib.Path("./doc").glob("*.md")])
    build_pandoc_pdf(out_doc.absolute(), docs_list, template_file)


if __name__ == '__main__':
    main()
