import { useContext, useEffect, useState } from "react";
import { api } from "../../util";
import { MultiContext } from "./Display";
import Button from "../atoms/Button";
import Icon from "../atoms/Icon";

const weekdays = ["S", "M", "T", "W", "Th", "F", "S"];

export default function Calendar({ className = "" }) {
  const multiCtx = useContext(MultiContext);
  const [deleting, setDeleting] = useState(false);
  const [copied, setCopied] = useState(false);

  const [favorited, setFavorited] = useState(false);
  const [count, setCount] = useState(0);

  const getJournal = () => {
    api(
      "get_journal",
      {
        name: multiCtx.currentJournal?.name,
        month: multiCtx.currentMonth,
        year: multiCtx.currentYear,
      },
      (data) => {
        let days_ = data.days;

        let offset = days_[0].weekdayInt;
        let offsetEnd = days_[days_.length - 1].weekdayInt;

        let filler = Array(offset + 1).fill({ filler: true });
        let fillerEnd = Array(Math.abs(offsetEnd - 7)).fill({ filler: true });

        days_ = days_.concat(fillerEnd);

        multiCtx.setDays(offset + 1 < 7 ? filler.concat(days_) : days_);
      }
    );
  };

  const deleteEntry = () => {
    api(
      "delete_entry",
      {
        journalName: multiCtx.currentJournal?.name,
        path: multiCtx.selectedDay?.entry?.path,
      },
      (data) => {
        multiCtx.setCurrentJournal(data.journal);
        multiCtx.setJournals(data.journals);
      }
    );
  };

  const toggleFavorite = () => {
    api(
      "toggle_favorite",
      {
        journalName: multiCtx.currentJournal?.name,
        path: multiCtx.selectedDay?.entry?.path,
      },
      (data) => setFavorited(data.entry.favorited)
    );
  };

  const copyNote = () => {
    navigator.clipboard.writeText(multiCtx.selectedDay?.entry?.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1000);
  };

  const prevMonth = () => {
    let month_ = multiCtx.currentMonth - 1;
    if (month_ === 0) {
      multiCtx.setCurrentYear(multiCtx.currentYear - 1);
      multiCtx.setCurrentMonth(12);
    } else {
      multiCtx.setCurrentMonth(month_);
    }
  };

  const nextMonth = () => {
    let month_ = multiCtx.currentMonth + 1;
    if (month_ === 13) {
      multiCtx.setCurrentYear(multiCtx.currentYear + 1);
      multiCtx.setCurrentMonth(1);
    } else {
      multiCtx.setCurrentMonth(month_);
    }
  };

  const resetMonth = () => {
    let today = new Date();
    multiCtx.setCurrentYear(today.getFullYear());
    multiCtx.setCurrentMonth(today.getMonth() + 1);
  };

  const isFilled = (day) => day.entry && !day.filler;

  const isHovered = (day) => multiCtx.hoveredDay?.id === day.id && !day.filler;

  const isSelected = (day) =>
    multiCtx.selectedDay?.id === day.id && !day.filler;

  const currentMonthSelected = () => {
    let today = new Date();
    return (
      multiCtx.currentMonth === today.getMonth() + 1 &&
      multiCtx.currentYear === today.getFullYear()
    );
  };

  useEffect(() => {
    multiCtx.currentJournal && getJournal();
  }, [multiCtx.currentJournal, multiCtx.currentMonth]);

  useEffect(() => {
    multiCtx.setSelectedDay(null);
  }, [multiCtx.currentMonth]);

  useEffect(() => {
    setCount(multiCtx.days.filter((x) => x.entry).length);
    currentMonthSelected() &&
      multiCtx.setSelectedDay(
        multiCtx.days.find((x) => x.day === new Date().getDate())
      );
  }, [multiCtx.days]);

  useEffect(() => {
    if (multiCtx.selectedDay && multiCtx.selectedDay?.entry) {
      setFavorited(multiCtx.selectedDay?.entry?.favorited);
    }
  }, [multiCtx.selectedDay]);

  return (
    <div className={className + " d-flex"}>
      <div className="m-auto">
        <div className="text-center mb-3">
          <div className="h5 m-0">
            {multiCtx.hoveredDay
              ? multiCtx.hoveredDay?.fullLabel
              : multiCtx.selectedDay
              ? multiCtx.selectedDay?.fullLabel
              : multiCtx.days.find((x) => !x.filler)?.monthLabel}
          </div>
          &nbsp;
          <span className="badge border-0">{`${count} Entr${
            count === 1 ? "y" : "ies"
          }`}</span>
        </div>
        <div className="between">
          <Button
            onClick={() => prevMonth()}
            icon="arrow-left"
            className="border-0"
          />
          {!currentMonthSelected() ? (
            <Button
              onClick={() => resetMonth()}
              icon="fast-forward-fill"
              className="blue border-0"
              text="Today"
            />
          ) : (
            <Button
              onClick={() => multiCtx.addEntry()}
              className="green border-0"
              icon="plus-lg"
              text="New"
            />
          )}
          <div>
            <Button
              disabled={currentMonthSelected()}
              onClick={() => nextMonth()}
              icon="arrow-right"
              className="border-0"
            />
          </div>
        </div>
        <div
          className="month mt-3"
          onMouseLeave={() => multiCtx.setHoveredDay(null)}>
          {weekdays.map((x) => (
            <div className="weekday mb-2">{x}</div>
          ))}
          {multiCtx.days.map((x) => (
            <div
              key={x.id}
              onClick={() =>
                multiCtx.setSelectedDay(
                  x.id === multiCtx.selectedDay?.id ? null : x
                )
              }
              onMouseEnter={() => multiCtx.setHoveredDay(x.filler ? null : x)}
              className={
                "day" +
                (x.filler
                  ? " filler"
                  : x?.entry?.favorited
                  ? " yellow-bg"
                  : "") +
                (isFilled(x) ? " filled" : "") +
                (isHovered(x) ? " hovered-day" : "") +
                (isSelected(x) ? " selected-day" : "")
              }></div>
          ))}
        </div>

        {multiCtx.selectedDay?.entry && (
          <>
            <hr />
            <div className="d-flex">
              <div className="mx-auto">
                <Button
                  onClick={() => toggleFavorite()}
                  className="yellow border-0"
                  icon={"star" + (favorited ? "-fill" : "")}
                />
                <Button
                  onClick={() => copyNote()}
                  className="border-0"
                  icon={copied ? "check-lg" : "copy"}
                />
                {deleting && (
                  <Button
                    onClick={() => deleteEntry()}
                    className="red border-0"
                    icon="question-lg"
                  />
                )}
                <Button
                  onClick={() => setDeleting(!deleting)}
                  className="red border-0"
                  icon="trash2"
                />
              </div>
            </div>
          </>
        )}
        <div className="mt-4">
          {multiCtx.days
            .filter((x) => x.entry && x.entry?.favorited)
            .map((y) => (
              <button className="entry-btn btn btn-sm">
                <div className="">
                  <Icon className="yellow" name="star-fill me-2" />
                  <span>{y.entry.nameFormatted}</span>
                </div>
                <span className="ms-2 badge ">{y.entry.journal}</span>
              </button>
            ))}
        </div>
      </div>
    </div>
  );
}
