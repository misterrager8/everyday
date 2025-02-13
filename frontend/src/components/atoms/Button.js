export default function Button({
  text,
  icon,
  onClick,
  size = "sm",
  className = "",
  type_ = "button",
  disabled = false,
}) {
  return (
    <button
      disabled={disabled}
      type={type_}
      onClick={onClick}
      className={className + " btn" + (size ? ` btn-${size}` : "")}>
      {icon && <i className={(text ? "me-2" : "ms-2") + " bi bi-" + icon}></i>}
      {text}
      {!text && <span>&nbsp;</span>}
    </button>
  );
}
