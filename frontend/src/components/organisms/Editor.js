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
    { format: `${selection.selected}`, label: "bold", icon: "type-bold" },
    { format: `${selection.selected}`, label: "italic", icon: "type-italic" },
    { format: `${selection.selected}`, label: "italic", icon: "type" },
    { format: `${selection.selected}`, label: "italic", icon: "link" },
    { format: `${selection.selected}`, label: "italic", icon: "file-break" },
    { format: `${selection.selected}`, label: "italic", icon: "list-ul" },
    { format: `${selection.selected}`, label: "italic", icon: "123" },
    { format: `${selection.selected}`, label: "italic", icon: "code-slash" },
    { format: `${selection.selected}`, label: "italic", icon: "image" },
    { format: `${selection.selected}`, label: "italic", icon: "type-h1" },
    {
      format: `${selection.selected}`,
      label: "italic",
      icon: "chevron-double-right",
    },
    { format: `${selection.selected}`, label: "italic", icon: "calendar" },
    { format: `${selection.selected}`, label: "italic", icon: "sort-down-alt" },
    { format: `${selection.selected}`, label: "italic", icon: "sort-down" },
    { format: `${selection.selected}`, label: "italic", icon: "three-dots" },
  ];

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
                className="border-0"
                icon={saved ? "check-lg" : "floppy2"}
              />
              <div className="btn-group ms-2">
                {formats.map((x) => (
                  <Button key={x.icon} icon={x.icon} />
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
      <hr />
      <div className="row">
        {["write", "split"].includes(view) && (
          <div className="col">
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
          <div className="col">
            <div
              id="reader"
              dangerouslySetInnerHTML={{
                __html: markdownit().render(content),
              }}></div>
          </div>
        )}
      </div>
    </div>
  );
}
