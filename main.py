import pathlib
import shutil
import datetime
import jinja2
import markdown2


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

        env = jinja2.Environment(
            loader=jinja2.DictLoader(
                {
                    "base": (site / "base.jinja2").read_text(),
                    "index": (site / "index.jinja2").read_text(),
                    "post": (site / "post.jinja2").read_text(),
                }
            )
        )

        posts = []
        print(f"{site=}")
        for site_file in site.iterdir():
            if site_file.suffix not in [".txt", ".jinja2"]:
                shutil.copy(site_file, deploy_site_dir)
                continue
            if site_file.suffix != ".txt":
                continue
            print(f"{site=}, {site_file=}")
            out = markdowner.convert(site_file.read_text())
            out.metadata["creation_date"] = datetime.datetime.strptime(
                out.metadata["creation_date"], "%Y-%m-%d"
            )
            file_out = (deploy_site_dir / site_file.name).with_suffix(".html")
            file_out.write_text(
                env.get_template("post").render(
                    title=out.metadata.get("title"),
                    out=out,
                    file_out_name=file_out.name,
                    posts=posts,
                )
            )
            posts.append((out, file_out.name))

        posts = sorted(
            posts, key=lambda x: x[0].metadata.get("creation_date"), reverse=True
        )

        index_html = env.get_template("index").render(
            title=site.name.capitalize(),
            posts=posts,
        )
        pathlib.Path(deploy_site_dir / "index.html").write_text(index_html)


if __name__ == "__main__":
    main()
