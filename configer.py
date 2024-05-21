from InquirerPy import prompt


def main():
    questions = [
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Select detection mode:',
            'default': '标准：被追踪对象离开画面时锁定',
            'choices': ['严格：画面中出现第二个人类时锁定', '标准：被追踪对象离开画面时锁定', '宽松'],
        },
        {
            'type': 'input',
            'name': 'delay',
            'message': 'Enter delay time (in seconds):',
            'validate': lambda val: val.isdigit() or 'Please enter a valid number',
        },
    ]

    answers = prompt(questions)

    if answers['confirm']:
        mode = answers['mode']
        delay = int(answers['delay'])
        print(f'Selected mode: {mode}')
        print(f'Delay time: {delay} seconds')
        # Continue with your program logic
    else:
        print('Operation cancelled.')


if __name__ == '__main__':
    main()
