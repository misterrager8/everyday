import Icon from "../atoms/Icon";

export default function Dropdown({
  text,
  target,
  icon,
  size = "sm",
  classNameBtn = "",
  classNameMenu = "",
  children,
  autoClose = true,
}) {
  return (
    <>
      <a
        data-bs-target={"#" + target}
        data-bs-toggle="dropdown"
        data-bs-auto-close={autoClose}
        className={
          classNameBtn + " btn dropdown-toggle" + (size ? ` btn-${size}` : "")
        }>
        {icon && <Icon name={icon} className={text ? "me-2" : ""} />}
        {text}
      </a>
      <div id={target} className={classNameMenu + " dropdown-menu"}>
        {children}
      </div>
    </>
  );
}
