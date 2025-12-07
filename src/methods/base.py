class VacData:
    def __init__(self, url, title, wage, exp, common_empl, work_hours, format_work, resp_number, work_schedule, company_name):
        self.url = url
        self.title = title
        self.wage = wage
        self.exp = exp
        self.common_empl = common_empl
        self.work_hours = work_hours
        self.format_work = format_work
        self.resp_number = resp_number
        self.work_schedule = work_schedule
        self.company_name = company_name

    def __str__(self):
        return f"{self.url}\n{self.title}\n{self.wage}\n{self.exp}\n{self.common_empl}\n{self.work_hours}\n{self.format_work}\n{self.resp_number}\n{self.work_schedule}\n"