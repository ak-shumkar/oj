from bs4 import BeautifulSoup
import requests
import random
from problem.models import Problem
from termcolor import colored


def scrape():
    try:
        pid = 1466 # random.randint(1, 1474)
        _pid = 'B' # random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        print(f'Scraping problem {pid}{_pid} ...')
        url = f'https://codeforces.com/problemset/problem/{str(pid)}/{_pid}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('div', {'class': 'title'}).text.split('.')[1].strip()
        time_limit = soup.find('div', {'class': 'time-limit'}).text.split('test')[1][0]
        memory_limit = soup.find('div', {'class': 'memory-limit'}).text.split('test')[1].split(' ')[0]
        divs = soup.find('div', {'class': 'problem-statement'})
        description = divs.findAll('div')[10].text

        input_format = soup.find('div', {'class': 'input-specification'}).text
        output_format = soup.find('div', {'class': 'output-specification'}).text

        sample_tests = soup.find('div', {'class': 'sample-tests'})
        test_samples = []
        for sample_test in sample_tests.findAll('div', {'class': 'sample-test'}):
            input_sample = sample_test.find('div', {'class': 'input'}).get_text().split('Input')[1].strip()
            output_sample = sample_test.find('div', {'class': 'output'}).text.split('Output')[1].strip()
            print('Here')

            sample = {
                'input': input_sample,
                'output': output_sample
            }
            test_samples.append(sample)
        try:
            clarification = soup.find('div', {'class': 'note'}).text
        except:
            clarification = None
            print('This problem does not have clarification')
    except Exception as e:
        print(colored(e, 'red', attrs=['bold']))

    else:
        try:
            Problem.objects.create(
                title=title,
                pid=_pid,
                description=description,
                difficulty=random.randint(1, 100),
                input_description=input_format,
                output_description=output_format,
                time_limit=int(time_limit) * 1000,
                memory_limit=int(memory_limit),
                author_id=1,
                contest_id=1,
                source='Codeforces',
                samples=test_samples,
                clarification=clarification
            )
        except Exception as e:
            print('CREATE ERROR : ', e)

        else:
            print(colored('Problem Created successfully !', 'green', attrs=['bold']))


def scrape_problems(count):
    for cnt in range(count):
        scrape()


