import requests
import sys
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

reg_id_start = 832500
reg_id_end = 832510
result_url = 'http://karresults.nic.in/resPUC_2018.asp'


def scrap_results():

    for reg_id in range(reg_id_start, reg_id_end):
        page = requests.post(result_url, data = {'reg': reg_id})
        soap = bs(page.text, "html.parser")
        user_detail_table = soap.find('table', id='details').find_all('tr')

        user_name = user_detail_table[0].find_all('td')[-1].text.strip()
        roll_number = user_detail_table[1].find_all('td')[-1].text.strip()

        all_panels = soap.find_all('div', class_='panel panel-primary')
        part_a_panel = all_panels[0].find('table')
        part_a_headings = part_a_panel.find_all('th')

        heading_subject_a = part_a_headings[0].text.strip()
        heading_theory_mark_a = part_a_headings[1].text.strip()
        heading_internal_mark_a = part_a_headings[2].text.strip()
        heading_total_mark_a = part_a_headings[3].text.strip()

        part_a_subject_list = part_a_panel.find_all('tr')

        marks_dict_a = {}

        for tr_tag in range(1, len(part_a_subject_list) - 1):
            td_tags = part_a_subject_list[tr_tag].find_all('td')

            subject = td_tags[0].text.strip()
            theory_mark = td_tags[1].text.strip()
            internal_mark = td_tags[2].text.strip() if not " " else "-"
            total_mark = td_tags[3].text.strip()
            marks_dict_a[subject] = [theory_mark,internal_mark,total_mark]


        part_a_total = part_a_subject_list[-1].find_all('td')[1].span.text.strip()


        part_b_panel = all_panels[1].find('table')
        part_b_headings = part_b_panel.find_all('th')

        heading_subject_b = part_b_headings[0].text.strip()
        heading_theory_mark_b = part_b_headings[1].text.strip()
        heading_practical_mark_b = part_b_headings[2].text.strip()
        heading_total_mark_b = part_b_headings[3].text.strip()

        part_b_subject_list = part_b_panel.find_all('tr')

        marks_dict_b = {}

        for tr_tag in range(1, len(part_b_subject_list) - 1):
            td_tags = part_b_subject_list[tr_tag].find_all('td')
            subject = td_tags[0].text.strip()
            theory_mark = td_tags[1].text.strip()
            practical_mark = td_tags[2].text.strip() if not " " else "-"
            total_mark = td_tags[3].text.strip()
            marks_dict_b[subject] = [theory_mark, internal_mark, total_mark]


        part_b_total = part_b_subject_list[-1].find_all('td')[1].span.text.strip()


        final_result_panel = soap.find('table', id="result").find_all('tr')
        grand_total  = final_result_panel[0].find_all('td')[1].text.strip()
        final_result = final_result_panel[1].find_all('td')[1].text.strip()


        user_detail = PrettyTable()
        user_detail.title = f"Result for {user_name} - ({roll_number})"
        user_detail.field_names = ['Part A Total', 'Part B Total', 'GRAND TOTAL MARKS', 'FINAL RESULT']
        user_detail.add_row([part_a_total, part_b_total, grand_total, final_result])

        result_table_a = PrettyTable()
        result_table_a.field_names = [heading_subject_a, heading_theory_mark_a, heading_internal_mark_a, heading_total_mark_a]
        result_table_a.title = "PART A"
        for subject_name, marks_field in marks_dict_a.items():
            temp = [subject_name]
            temp.extend(marks_field)
            result_table_a.add_row(temp)

        result_table_b = PrettyTable()
        result_table_b.field_names = [heading_subject_b, heading_theory_mark_b, heading_practical_mark_b, heading_total_mark_b]
        result_table_b.title = "PART B"

        for subject_name, marks_field in marks_dict_b.items():
            temp = [subject_name]
            temp.extend(marks_field)
            result_table_b.add_row(temp)

        with open('results.txt', 'a', encoding='utf-8') as infile:
            print(user_detail, file=infile)
            print(result_table_a, file=infile)
            print(result_table_b, file=infile, end="\n\n\n\n")
            print("----------------------------------------------------------------------", file=infile, end="\n\n\n\n")

    return True

if __name__ == '__main__':
    sys.stdout.write('Wait. Data is being scrapped...')
    sys.stdout.flush()
    finished = scrap_results()
    if finished:
        print('Finished! Check the results.txt file!')
