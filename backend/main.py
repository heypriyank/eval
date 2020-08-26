class Run:

    def __init__(self, link):
        import requests
        self.new_dict = {
             "Jan": 'January',
             "Feb": 'February',
             "Mar": 'March',
             "Apr": 'April',
             "May": 'May',
             "Jun": 'June',
             "Jul": 'July',
             "Aug": 'August',
             "Sep": 'September',
             "Oct": 'October',
             "Nov": 'November',
             "Dec": 'December'
         }

        page = requests.get(link)
        self.page_json = page.json()

    def readable(self):
        out_string = ''
        for x in range(len(self.page_json["paid"])):
            if self.page_json["paid"][x]['confName'] != '':
                t = self.page_json["paid"][x]["confName"]
                out_string += f'"{t.strip()}", '
            else:
                out_string += 'Conference Name Not Available, '
            if self.page_json["paid"][x]['confStartDate'] != '':
                new = self.page_json["paid"][x]['confStartDate'].split(',')
                date = new[0][:2]
                year = new[1]
                month = new[0][3:]
                if month in self.new_dict:
                    out_string += self.new_dict[month]
                else:
                    out_string += month
                out_string += f' {date},{year}, '
            else:
                out_string += 'Date Not Available, '
            if self.page_json["paid"][x]['city'] != '':
                out_string += self.page_json["paid"][x]['city'] + ', '
            if self.page_json["paid"][x]['state'] != '':
                out_string += self.page_json["paid"][x]['state'] + ', '
            if self.page_json["paid"][x]['country'] != '':
                out_string += self.page_json["paid"][x]['country'] + ', '
            out_string += self.page_json["paid"][x]['entryType'] + '. '
            out_string += f'"{self.page_json["paid"][x]["confUrl"]}"\n'

        for x in range(len(self.page_json["free"])):
            if self.page_json["free"][x]['confName'] != '':
                t = self.page_json["free"][x]["confName"]
                out_string += f'"{t.strip()}", '
            else:
                out_string += 'Conference Name Not Available, '
            if self.page_json["free"][x]['confStartDate'] != '':
                new = self.page_json["free"][x]['confStartDate'].split(',')
                date = new[0][:2]
                year = new[1]
                month = new[0][3:]
                if month in self.new_dict:
                    out_string += self.new_dict[month]
                else:
                    out_string += month
                out_string += f' {date},{year}, '
            else:
                out_string += 'Date Not Available, '
            if self.page_json["free"][x]['city'] != '':
                out_string += self.page_json["free"][x]['city'] + ', '
            if self.page_json["free"][x]['state'] != '':
                out_string += self.page_json["free"][x]['state'] + ', '
            if self.page_json["free"][x]['country'] != '':
                out_string += self.page_json["free"][x]['country'] + ', '
            out_string += self.page_json["free"][x]['entryType'] + '. '
            out_string += f'"{self.page_json["free"][x]["confUrl"]}"\n'

            return out_string

    def repetitions(self):
        out_string = ''
        rep = {}
        repeat_id_paid = []
        repeat_id_free = []

        for index in range(len(self.page_json["paid"])):
            if self.page_json["paid"][index]["conference_id"] in rep:
                repeat_id_paid.append(rep[self.page_json["paid"][index]["conference_id"]])
                rep[self.page_json["paid"][index]["conference_id"]] = index
                repeat_id_paid.append(rep[self.page_json["paid"][index]["conference_id"]])
            else:
                rep[self.page_json["paid"][index]["conference_id"]] = index

        rep.clear()

        for index in range(len(self.page_json["free"])):
            if self.page_json["free"][index]["conference_id"] in rep:
                repeat_id_free.append(rep[self.page_json["free"][index]["conference_id"]])
                rep[self.page_json["free"][index]["conference_id"]] = index
                repeat_id_free.append(rep[self.page_json["free"][index]["conference_id"]])
            else:
                rep[self.page_json["free"][index]["conference_id"]] = index

        for elem in range(0, len(repeat_id_paid), 2):
            if self.page_json["paid"][repeat_id_paid[elem]] == self.page_json["paid"][repeat_id_paid[elem + 1]]:
                out_string += f'Exact duplicates found at indices {repeat_id_paid[elem]} & {repeat_id_paid[elem + 1]} of paid section, with ' \
                              f'title "{self.page_json["paid"][repeat_id_paid[elem]]["confName"]}"\n '
            else:
                out_string += f'Semantic duplicates found at indices {repeat_id_paid[elem]} & {repeat_id_paid[elem + 1]} of paid section, ' \
                              f'with titles "{self.page_json["paid"][repeat_id_paid[elem]]["confName"]}" & "{self.page_json["paid"][repeat_id_paid[elem + 1]]["confName"]}"\n '

        for elem in range(0, len(repeat_id_free), 2):
            if self.page_json["paid"][repeat_id_free[elem]] == self.page_json["paid"][repeat_id_free[elem + 1]]:
                out_string += f'Exact duplicates found at indices {repeat_id_free[elem]} & {repeat_id_free[elem + 1]} of free section, with ' \
                              f'title "{self.page_json["free"][repeat_id_free[elem]]["confName"]}"\n '
            else:
                out_string += f'Semantic duplicates found at indices {repeat_id_free[elem]} & {repeat_id_free[elem + 1]} of free section.  ' \
                              f'with titles "{self.page_json["free"][repeat_id_free[elem]]["confName"]}" & "{self.page_json["free"][repeat_id_free[elem + 1]]["confName"]}"\n '

        return out_string


obj = Run('https://o136z8hk40.execute-api.us-east-1.amazonaws.com/dev/get-list-of-conferences')
print(obj.readable())
print(obj.repetitions())
