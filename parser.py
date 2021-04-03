import random
import requests
import re
import pprint
import string


def find_all_forms(source):
    pattern = '<form.*?id="frma.*?".*?(.*?)</form>'
    forms = re.findall(pattern, source, re.DOTALL)

    return forms


def find_all_fields(forms):
    pattern = '\stype="(.*?)".+?name="(.*?)".+?value="(.*?)"'
    selected_fields = ''
    max_fields = 100

    for form in forms:
        fields = [{'type': f_type, 'name': f_name, 'value': f_value} for f_type, f_name, f_value in re.findall(pattern, form, re.DOTALL)]
        #fields = re.findall(pattern, forms, re.DOTALL)
        if fields and len(fields) <= max_fields:
            max_fields = len(fields)
            selected_fields = fields

    return selected_fields


def send_fake_request(fields):
    for field in fields:
        if field['type'] == 'text' and not field['value']:
            letters = string.ascii_uppercase
            field['value'] = ''.join(random.choice(letters) for i in range(10))
        elif field['type'] == 'tel' and not field['value']:
            letters = string.digits
            field['value'] = ''.join(random.choice(letters) for i in range(10))
        elif not field['value']:
            letters = string.ascii_uppercase
            field['value'] = ''.join(random.choice(letters) for i in range(10))

    for field in fields:
        print('type = ', field['type'], ', name = ', field['name'], ', value = ', field['value'])


def main():
    url = 'https://lite5.ru/'
    #url = 'https://abcgarant.ru/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

    r = requests.get(url, headers)

    if r.status_code == 200:
        print('Status code = ', r.status_code)

        forms = find_all_forms(r.text)
        if forms:
            print('Total forms = ', len(forms))
            fields = find_all_fields(forms)
            if fields:
                send_fake_request(fields)
            else:
                print('No fields were found')
        else:
            print('Forms not found on this page - ', url)


# Start main prg
main()
