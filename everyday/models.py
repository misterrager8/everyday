from calendar import Calendar
import datetime
import pathlib
import shutil

import frontmatter

from everyday import config


class Journal:
    def __init__(self, name):
        self.name = name

    @property
    def path(self):
        return config.HOME_DIR / self.name

    @property
    def entries(self):
        return [Entry(i) for i in self.path.glob("**/*.txt")]

    def get_calendar(self, month, year):
        days_ = Calendar(6).itermonthdates(year, month)
        month_ = []
        for i in days_:
            if i.month == month and i.year == year and i <= datetime.date.today():
                match = [
                    j
                    for j in self.entries
                    if j.date_created.strftime("%y%m%d") == i.strftime("%y%m%d")
                ]
                month_.append(
                    {
                        "id": i.strftime("%y%m%d"),
                        "year": i.year,
                        "month": i.month,
                        "day": i.day,
                        "weekdayInt": i.weekday(),
                        "monthLabel": i.strftime("%B %Y"),
                        "fullLabel": i.strftime("%B %-d, %Y"),
                        "entry": (match[0].todict() if len(match) > 0 else None),
                    }
                )

        return month_

    def add(self):
        self.path.mkdir()

    def add_entry(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        entry_ = pathlib.Path(self.path / f"{today}.txt")
        if not entry_.exists():
            entry_.touch()

    @classmethod
    def all(cls):
        return [Journal(i.name) for i in config.HOME_DIR.iterdir() if i.is_dir()]

    @classmethod
    def rename(cls, old_name, new_name):
        journal_ = Journal(old_name)
        journal_.path.rename(config.HOME_DIR / new_name)

        return journal_

    def delete(self):
        shutil.rmtree(self.path)

    def todict(self):
        return {
            "name": self.name,
            "path": str(self.path),
            "count": len(self.entries),
        }


class Entry:
    def __init__(self, path):
        self.path = pathlib.Path(path)

    @property
    def frontmatter(self):
        _ = frontmatter.load(self.path)
        if not frontmatter.check(self.path):
            _.metadata.update({"favorited": False})

        return _

    @property
    def date_created(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.path.stat().st_birthtime)

    @property
    def last_modified(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.path.stat().st_mtime)

    @property
    def favorited(self):
        return self.frontmatter.get("favorited")

    @property
    def formatted_name(self):
        file_name = datetime.datetime.strptime(self.path.stem, "%Y-%m-%d")
        formatted = file_name.strftime("%-m/%-d")

        return formatted

    @property
    def content(self):
        return self.frontmatter.content

    def edit(self, content: str):
        _ = self.frontmatter
        _.content = content
        self.edit_frontmatter(_)

    def edit_frontmatter(self, metadata: dict):
        new_data = frontmatter.dumps(metadata)
        open(self.path, "w").write(new_data)

    def toggle_favorite(self):
        _ = self.frontmatter
        _.metadata.update({"favorited": not _.metadata.get("favorited")})
        self.edit_frontmatter(_)

    def delete(self):
        pathlib.Path(self.path).unlink()

    @classmethod
    def get_all_favorites(cls):
        return [Entry(i) for i in config.HOME_DIR.glob("**/*.txt")]

    def todict(self) -> dict:
        return {
            "name": self.path.stem,
            "nameFormatted": self.formatted_name,
            "path": str(self.path),
            "journal": self.path.parent.name,
            "content": self.content,
            "favorited": self.favorited,
            "date_created": self.date_created.strftime("%-m/%-d/%y @ %-I:%M %p"),
            "last_modified": self.last_modified.strftime("%-m/%-d/%y @ %-I:%M %p"),
        }
