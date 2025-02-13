from calendar import Calendar
import datetime
import pathlib
import shutil

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
                        "entry": (
                            {"content": match[0].content, "path": str(match[0].path)}
                            if len(match) > 0
                            else None
                        ),
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
        }


class Entry:
    def __init__(self, path):
        self.path = path

    @property
    def date_created(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.path.stat().st_birthtime)

    @property
    def content(self):
        return open(self.path).read()

    def edit(self, content):
        open(self.path, "w").write(content)

    def delete(self):
        pathlib.Path(self.path).unlink()
