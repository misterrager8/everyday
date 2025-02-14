import { createContext, Fragment, useEffect, useState } from "react";
import { api } from "../../util";
import Button from "../atoms/Button";
import Dropdown from "../molecules/Dropdown";
import Calendar from "./Calendar";
import Editor from "./Editor";
import Icon from "../atoms/Icon";

export const MultiContext = createContext();

export default function Display({ className = "" }) {
  const [theme, setTheme] = useState(
    localStorage.getItem("everyday-theme") || "light"
  );
  const [journals, setJournals] = useState([]);
  const [currentJournal, setCurrentJournal] = useState(
    JSON.parse(localStorage.getItem("everyday-most-recent-journal")) || null
  );

  const [renamed, setRenamed] = useState(false);

  const [currentJournalName, setCurrentJournalName] = useState("");
  const onChangeCurrentJournalName = (e) =>
    setCurrentJournalName(e.target.value);

  const [newJournalName, setNewJournalName] = useState("");
  const onChangeNewJournalName = (e) => setNewJournalName(e.target.value);

  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth() + 1);
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());

  const [days, setDays] = useState([]);
  const [hoveredDay, setHoveredDay] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);

  const [deleting, setDeleting] = useState(false);
  const [favorites, setFavorites] = useState([]);

  const resetAll = () => {
    setSelectedDay(null);
    setCurrentJournal(null);
    getJournals();
  };

  const getJournals = () => {
    api("get_journals", {}, (data) => {
      setFavorites(data.entries);
      setJournals(data.journals);
    });
  };

  const renameJournal = (e) => {
    e.preventDefault();
    api(
      "rename_journal",
      {
        name: currentJournal.name,
        newName: currentJournalName,
      },
      (data) => {
        setCurrentJournal(data.journal);
        setJournals(data.journals);
        setRenamed(true);
        setTimeout(() => setRenamed(false), 1000);
      }
    );
  };

  const addEntry = () => {
    api(
      "add_entry",
      {
        name: currentJournal.name,
      },
      (data) => {
        setCurrentJournal(data.journal);
        setJournals(data.journals);
      }
    );
  };

  const addJournal = (e) => {
    e.preventDefault();
    api(
      "add_journal",
      {
        name: newJournalName,
      },
      (data) => {
        setCurrentJournal(data.journal);
        setJournals(data.journals);
        setNewJournalName("");
      }
    );
  };

  const deleteJournal = () => {
    api(
      "delete_journal",
      {
        name: currentJournal?.name,
      },
      (data) => {
        setCurrentJournal(null);
        setJournals(data.journals);
      }
    );
  };

  useEffect(() => {
    localStorage.setItem("everyday-theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem(
      "everyday-most-recent-journal",
      JSON.stringify(currentJournal)
    );
  }, [currentJournal]);

  const contextValue = {
    journals: journals,
    setJournals: setJournals,
    getJournals: getJournals,

    currentJournal: currentJournal,
    setCurrentJournal: setCurrentJournal,

    resetAll: resetAll,
    addEntry: addEntry,

    theme: theme,
    setTheme: setTheme,

    currentMonth: currentMonth,
    setCurrentMonth: setCurrentMonth,

    currentYear: currentYear,
    setCurrentYear: setCurrentYear,

    days: days,
    setDays: setDays,
    hoveredDay: hoveredDay,
    setHoveredDay: setHoveredDay,
    selectedDay: selectedDay,
    setSelectedDay: setSelectedDay,

    favorites: favorites,
    setFavorites: setFavorites,
  };

  useEffect(() => {
    getJournals();
  }, []);

  useEffect(() => {
    setCurrentJournalName(currentJournal ? currentJournal?.name : "");
  }, [currentJournal]);

  return (
    <MultiContext.Provider value={contextValue}>
      <div className={className + " col-2 border-end"}>
        <div className="between">
          <div className="btn-group btn-group-sm">
            <Dropdown
              autoClose="outside"
              icon={renamed ? "check-lg" : "journal-album"}
              target="journals"
              classNameMenu="text-center"
              classNameBtn="border-0">
              {currentJournal && (
                <div className="mx-2">
                  <Button
                    className="w-100"
                    onClick={() => resetAll()}
                    icon="house-fill"
                  />
                  <hr className="my-2" />
                </div>
              )}
              {journals.map((x) => (
                <a
                  key={x.name}
                  onClick={() => setCurrentJournal(x)}
                  className={
                    "dropdown-item between" +
                    (currentJournal?.name === x.name ? " active" : "")
                  }>
                  <span>{x.name}</span>
                  <span className="badge ms-4">{x.count}</span>
                </a>
              ))}
            </Dropdown>
            {!currentJournal ? (
              <form onSubmit={(e) => addJournal(e)}>
                <input
                  className="form-control form-control-sm fst-italic"
                  autoComplete="off"
                  value={newJournalName}
                  onChange={onChangeNewJournalName}
                  placeholder="New Journal"
                />
              </form>
            ) : (
              <form onSubmit={(e) => renameJournal(e)} className="input-group">
                <input
                  className="form-control form-control-sm fst-italic"
                  autoComplete="off"
                  value={currentJournalName}
                  onChange={onChangeCurrentJournalName}
                />
              </form>
            )}
          </div>
          <Button
            className="border-0"
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            icon={theme === "light" ? "sun-fill" : "moon-fill"}
          />
        </div>
        {currentJournal && (
          <>
            <hr />
            <Calendar />
          </>
        )}
        {!currentJournal && (
          <div className="mt-4">
            {favorites.map((y) => (
              <button className="entry-btn btn btn-sm">
                <div className="">
                  <Icon className="yellow" name="star-fill me-2" />
                  <span>{y.nameFormatted}</span>
                </div>
                <span className="ms-2 badge ">{y.journal}</span>
              </button>
            ))}
          </div>
        )}
        {currentJournal && (
          <div className="bottom p-4">
            <div className="btn-group w-100">
              <Button
                text="Delete Journal"
                className="red border-0"
                icon="trash2"
                onClick={() => setDeleting(!deleting)}
              />
              {deleting && (
                <Button
                  className="red border-0"
                  icon="question-lg"
                  onClick={() => deleteJournal()}
                />
              )}
            </div>
          </div>
        )}
      </div>
      <div className="col-10">
        {selectedDay && selectedDay?.entry && <Editor />}
      </div>
    </MultiContext.Provider>
  );
}
