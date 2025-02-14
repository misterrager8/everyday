import { useContext, useEffect, useState } from "react";
import { MultiContext } from "./Display";
import Button from "../atoms/Button";
import markdownit from "markdown-it";
import { api } from "../../util";
import Icon from "../atoms/Icon";

export default function Editor({ className = "" }) {
  const multiCtx = useContext(MultiContext);

  const [view, setView] = useState(
    localStorage.getItem("everyday-view") || "split"
  );
  const [saved, setSaved] = useState(false);

  const [content, setContent] = useState("");
  const onChangeContent = (e) => setContent(e.target.value);

  const [selection, setSelection] = useState({
    start: 0,
    end: 0,
    selected: "",
  });

  useEffect(() => {
    if (multiCtx.selectedDay && multiCtx.selectedDay?.entry) {
      setContent(multiCtx.selectedDay?.entry?.content);
    }
  }, [multiCtx.selectedDay]);

  useEffect(() => {
    localStorage.setItem("everyday-view", view);
  }, [view]);

  const editEntry = () => {
    api(
      "edit_entry",
      {
        path: multiCtx.selectedDay?.entry?.path,
        content: content,
      },
      (data) => {
        setSaved(true);
        setTimeout(() => setSaved(false), 1000);
      }
    );
  };

  const views = [
    { value: "write", icon: "pencil" },
    { value: "read", icon: "eye" },
    { value: "split", icon: "layout-split" },
  ];

  const formats = [
    {
      icon: "type-bold",
      label: "bold",
      format: `**${selection.selected}**`,
    },
    {
      icon: "type-italic",
      label: "italic",
      format: `*${selection.selected}*`,
    },
    {
      icon: "type-h1",
      label: "heading",
      format: `### ${selection.selected}`,
    },
    {
      icon: "sort-alpha-down",
      label: "sort",
      format: `${selection.selected.split("\n").toSorted().join("\n")}`,
    },
    {
      icon: "sort-alpha-up-alt",
      label: "sort-reverse",
      format: `${selection.selected
        .split("\n")
        .toSorted()
        .reverse()
        .join("\n")}`,
    },
    {
      icon: "list-ul",
      label: "bullet-list",
      format: `- ${selection.selected.split("\n").join("\n- ")}`,
    },
    {
      icon: "type-strikethrough",
      label: "strikethrough",
      format: `~~${selection.selected}~~`,
    },
    {
      icon: "check-lg",
      label: "check",
      format: `✓`,
    },
    {
      icon: "code-slash",
      label: "code-block",
      format: `\`\`\`${selection.selected}\`\`\``,
    },
    {
      icon: "code",
      label: "code-inline",
      format: `\`${selection.selected}\``,
    },
    {
      icon: "superscript",
      label: "superscript",
      format: `<sup>[${selection.selected}]</sup>`,
    },
    {
      icon: "highlighter",
      label: "highlight",
      format: `<mark>${selection.selected}</mark>`,
    },
    {
      icon: "alarm",
      label: "time",
      format: `${new Date().getHours()}:${new Date().getMinutes()} ${new Date()
        .toLocaleTimeString()
        .slice(-2)}`,
    },
    {
      icon: "image",
      label: "image",
      format: `![${selection.selected}]()`,
    },
    {
      icon: "link",
      label: "link",
      format: `[${selection.selected}]()`,
    },
    {
      icon: "type",
      label: "capitalize",
      format: `${
        selection.selected.charAt(0).toUpperCase() + selection.selected.slice(1)
      }`,
    },
    {
      icon: "alphabet-uppercase",
      label: "allcaps",
      format: `${selection.selected.toUpperCase()}`,
    },
    {
      icon: "alphabet",
      label: "alllower",
      format: `${selection.selected.toLowerCase()}`,
    },
    {
      icon: "indent",
      label: "indent",
      format: `  ${selection.selected}`,
    },
  ];

  const copyFormat = (format) => {
    let format_ = formats.filter((x) => x.label === format)[0];
    let new_ =
      content.substring(0, selection.start) +
      format_.format +
      content.substring(selection.end, content.length);
    setContent(new_);
  };

  const getSelection = () => {
    let elem = document.getElementById("editor");

    let start = elem.selectionStart;
    let end = elem.selectionEnd;
    let selected = content.substring(start, end);

    setSelection({ start: start, end: end, selected: selected });
  };

  return (
    <div className={className}>
      <div className="between">
        <div>
          {view !== "read" && (
            <>
              <Button
                onClick={() => editEntry()}
                className="green"
                icon={saved ? "check-lg" : "floppy2"}
              />
              <div className="btn-group ms-2">
                {formats.map((x) => (
                  <Button
                    onClick={() => copyFormat(x.label)}
                    key={x.icon}
                    icon={x.icon}
                  />
                ))}
              </div>
            </>
          )}
        </div>
        <div className="btn-group">
          {views.map((x) => (
            <Button
              key={x.value}
              onClick={() => setView(x.value)}
              className={view === x.value ? "active" : ""}
              icon={x.icon}
            />
          ))}
        </div>
      </div>
      <hr className="mb-0" />
      <div className="between my-1">
        &nbsp;
        <span className="badge border-0">
          <Icon name="pencil me-2" />
          {multiCtx.selectedDay?.entry?.last_modified}
        </span>
      </div>
      <div className="row">
        {["write", "split"].includes(view) && (
          <div className={"col" + (view === "write" ? "-12" : "-6")}>
            <textarea
              id="editor"
              onMouseUp={() => getSelection()}
              placeholder="..."
              style={{ height: "85vh" }}
              rows={20}
              className="form-control form-control fst-italic"
              value={content}
              onChange={onChangeContent}></textarea>
          </div>
        )}
        {["read", "split"].includes(view) && (
          <div className={"col" + (view === "read" ? "-12" : "-6")}>
            <div
              style={{ height: "85vh", overflowY: "scroll" }}
              id="reader"
              dangerouslySetInnerHTML={{
                __html: markdownit({ html: true }).render(content),
              }}></div>
          </div>
        )}
      </div>
    </div>
  );
}
