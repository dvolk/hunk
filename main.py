import markdown2
import pathlib
import shutil
import jinja2


def main():
    pathlib.Path("./sites").mkdir(exist_ok=True)
    pathlib.Path("./deploy").mkdir(exist_ok=True)

    sites = [x.name for x in pathlib.Path("./sites").iterdir() if x.is_dir()]
    for site in sites:
        print(site)
        depl_site_dir = pathlib.Path("./deploy") / site
        shutil.rmtree(depl_site_dir, ignore_errors=True)
        depl_site_dir.mkdir()

        site_files = (pathlib.Path("./sites") / site).iterdir()
        site_files = sorted(site_files, reverse=True)

        post_template = jinja2.Template(
            (pathlib.Path("./sites/") / site / "post.jinja2").read_text()
        )
        posts = []

        for site_file in site_files:
            if site_file.suffix != ".txt":
                continue
            file_in = site_file.read_text()
            out_md = markdown2.markdown(
                file_in,
                extras=[
                    "metadata",
                    "code-friendly",
                    "fenced-code-blocks",
                    "footnotes",
                    "mermaid",
                ],
            )
            file_out = (depl_site_dir / site_file.name).with_suffix(".html")
            file_out.write_text(
                post_template.render(
                    out_md=out_md, m=out_md.metadata, file_out_name=file_out.name
                )
            )
            title = out_md.metadata.get("title", file_out.name)
            posts.append((title, file_out.name))
            print(file_out)

        index_template = jinja2.Template(
            (pathlib.Path("./sites") / site / "index.jinja2").read_text()
        )
        index_html = index_template.render(posts=posts)
        pathlib.Path(depl_site_dir / "index.html").write_text(index_html)

        for site_file in site_files:
            if site_file.suffix not in [".txt", ".jinja2"]:
                shutil.copy(site_file, depl_site_dir)


if __name__ == "__main__":
    main()
