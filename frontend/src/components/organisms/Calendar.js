import { useContext, useEffect, useState } from "react";
import { api } from "../../util";
import { MultiContext } from "./Display";
import Button from "../atoms/Button";

export default function Calendar({ className = "" }) {
  const multiCtx = useContext(MultiContext);
  const [deleting, setDeleting] = useState(false);
  const [copied, setCopied] = useState(false);

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
        let filler = Array(offset + 1).fill({ filler: true });

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
    let today = new Date();
    currentMonthSelected() &&
      multiCtx.setSelectedDay(multiCtx.days[multiCtx.days.length - 1]);
  }, [multiCtx.days]);

  return (
    <div className={className + " d-flex"}>
      <div className="m-auto">
        <div className="text-center h5">
          {multiCtx.hoveredDay
            ? multiCtx.hoveredDay?.fullLabel
            : multiCtx.selectedDay
            ? multiCtx.selectedDay?.fullLabel
            : multiCtx.days[multiCtx.days.length - 1]?.monthLabel}
          &nbsp;
        </div>
        <div className="between pe-4">
          <Button
            onClick={() => prevMonth()}
            icon="arrow-left"
            className="border-0"
          />
          {!currentMonthSelected() ? (
            <Button
              onClick={() => resetMonth()}
              icon="record-fill"
              className="border-0"
              text="Today"
            />
          ) : (
            <Button
              onClick={() => multiCtx.addEntry()}
              className="border-0"
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
          {multiCtx.days.map((x) => (
            <div
              key={x.id}
              onClick={() =>
                multiCtx.setSelectedDay(
                  x.id === multiCtx.selectedDay?.id ? null : x
                )
              }
              onMouseEnter={() => multiCtx.setHoveredDay(x)}
              className={
                "day" +
                (x.filler ? " filler" : "") +
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
              <div className="btn-group mx-auto">
                <Button className="border-0" icon="star" />
                <Button
                  onClick={() => copyNote()}
                  className="border-0"
                  icon={copied ? "check-lg" : "copy"}
                />
                {deleting && (
                  <Button
                    onClick={() => deleteEntry()}
                    className="border-0"
                    icon="question-lg"
                  />
                )}
                <Button
                  onClick={() => setDeleting(!deleting)}
                  className="border-0"
                  icon="trash2"
                />
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
