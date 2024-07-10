import markdown2
import pathlib
import shutil
import jinja2


def main():
    markdowner = markdown2.Markdown(
        extras=[
            "metadata",
            "code-friendly",
            "fenced-code-blocks",
            "footnotes",
            "mermaid",
        ],
    )

    (sites_dir := pathlib.Path("./sites")).mkdir(exist_ok=True)
    (deploys_dir := pathlib.Path("./deploy")).mkdir(exist_ok=True)

    for site in sites_dir.iterdir():
        deploy_site_dir = deploys_dir / site.name
        shutil.rmtree(deploy_site_dir, ignore_errors=True)
        deploy_site_dir.mkdir()

        post_template = jinja2.Template((site / "post.jinja2").read_text())
        index_template = jinja2.Template((site / "index.jinja2").read_text())

        posts = []
        print(f"{site=}")
        for site_file in sorted(site.iterdir(), reverse=True):
            if site_file.suffix not in [".txt", ".jinja2"]:
                shutil.copy(site_file, deploy_site_dir)
                continue
            if site_file.suffix != ".txt":
                continue
            print(f"{site=}, {site_file=}")
            out = markdowner.convert(site_file.read_text())
            file_out = (deploy_site_dir / site_file.name).with_suffix(".html")
            file_out.write_text(
                post_template.render(
                    out=out,
                    file_out_name=file_out.name,
                    posts=posts,
                )
            )
            posts.append((out, file_out.name))

        index_html = index_template.render(posts=posts)
        pathlib.Path(deploy_site_dir / "index.html").write_text(index_html)


if __name__ == "__main__":
    main()
