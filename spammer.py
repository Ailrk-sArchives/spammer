"""
Require a file named .spamming_list with target email address listed,
two environment variable MAIL_USER and MAIL_PWD
"""

import smtplib, os, sys, getopt
from email.mime.text import MIMEText
import email.header


class Spammer:
    """ Spammer handles with email sending """
    mail_user = ''
    mail_pwd = ''
    msg = None
    subject = ''
    _from = ''
    _to_list = ''
    

    def __init__(self, msg='', _to_list=[], subject=''):
        """ get MAIL_USER and MAIL_PWD from env """
        try:
#            self.mail_user = os.environ['MAIL_USER']
#            self.mail_pwd = os.environ['MAIL_PWD']

            self.mail_user = "jimmy123good@gmail.com"
            self.mail_pwd = "jimmyyao1998"

        except KeyError:
            print('KeyError. Make sure you have MAIL_USER and MAIL_PWD as environmental variables')
    
        # set msg content
        if isinstance(msg, str) and msg != None:
            self.msg = MIMEText(msg)
        else:
            raise TypeError('Error! msg must be non-empty string')

        # set to_spam_list
        if isinstance(_to_list, list) and _to_list:
            self._to_list = _to_list
        else:
            raise TypeError('Error! _to_list must be non-empty list')

        self._from = self.mail_user
        self.subject = str(subject)

    def send(self):
        self.__set_msg()

        if self.__prerequisite_checking():
            self.__send_msg()
        else:
            print('Spammer need infomation with integrity')
            sys.exit(1)

    def __set_msg(self):
       	self.msg['Subject'] = email.header.Header(self.subject, 'utf-8')
        self.msg['From'] = email.header.Header(self._from,'utf-8')
        self.msg['To'] = email.header.Header(','.join(self._to_list), 'utf-8')

    def __send_msg(self):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.login(self.mail_user, self.mail_pwd)
            s.sendmail(self._from, self._to_list, self.msg.as_string())
            s.close()
            print ('Sucessfully sent')
            
        except smtplib.SMTPException as e:
            raise e
            print ('failed to send')

    def __prerequisite_checking(self):
        """ checking if the spam is ready to go """
        if self.mail_pwd != '' and self.mail_user != '' and self.msg != None \
                and self._from != '' and  self.subject != '' and self._to_list:
            return True
        return False


class Manager:
    config = False
    list_path = ''
    text_path = ''

    mail_user = ''
    mail_pwd = ''

    def __init__(self):
        self.__check_args()
        # try to open mail_list and text
        try:
            with open(self.list_path, 'r') as list_fp, \
                    open(self.text_path, 'r') as text_fp:
                # get msg string 
                msg = text_fp.read()
                subject = input('What subject you want it be?>')
                _to_list = [line.strip() for line in list_fp]
                print (_to_list)

                spammer = Spammer(msg=msg, _to_list=_to_list, subject=subject)
                spammer.send()
        except IOError as e:
            print ('Error: %s' % e.strerror)

        
    def configruation(self):
        print()
        print('Starting a new spamming? You such an asshole')
        print()
        print('current status:')
        MAIL_USER = MAIL_PWD = None
        try:
            MAIL_USER = os.environ['MAIL_USER']
            MAIL_PWD = os.environ['MAIL_PWD']
        except KeyError:
            pass

        print('---MAIL_USER:    ' + (MAIL_USER or 'no value'))
        print('---MAIL_PWD:     ' + (MAIL_PWD or 'no value'))
        print('-------------------------------------------------')

        modify = input('modify? ')

        if modify:
            if self.__ask('modify MAIL_USER?'):self.__update_env_var('MAIL_USER')
            if self.__ask('modify MAIL_PWD?'):self.__update_env_var('MAIL_PWD')
            
        else:
            print('Good Luck')
        sys.exit(0)

    def __ask(self, msg):
        while True:
            ans = input(msg + '(y/n)') 
            if ans == 'y':
                return True
            elif ans == 'n':
                return False
            else:
                print('please answer \'y\' or \'n\'')

    def __update_env_var(self, var):
        os.environ[var] = input('> ')
            
        
    def __check_args(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hcl:t:', ['help','config', \
                    'list_path', 'text_path'])

            for o, a in opts:
                if o in ('-h', '--help'):
                    self.__usage()
                elif o in ('-c', '--config'):
                    self.configruation()       
                elif o in ('-l', '--list_path'):
                    self.list_path = str(a)
                elif o in ('-t', '--text_path'):
                    self.text_path = str(a)
                else:
                    assert False, 'Unhandled argument'
                   
        except getopt.GetoptError as e:
            print(e)
    
    @staticmethod
    def __usage():
        print('SPAMMER ---The utimate business booster')
        print('usage:')
        print('     spammer [options] <args>')
        print
        print('options:')
        print('     config the spamer info')
        print('         -h --help')
        print('         -c --config')
        print('         -l --list_path <file_path>')
        print('         -t --text_path <file_path>')
        sys.exit(0)



if __name__ == '__main__':
    spam_manager = Manager()
