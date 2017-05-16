#!/usr/bin/env python3
import sys, os
import re
import argparse
 
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch
 
    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
 
    return _getch
 
getch = _find_getch()
output_languages = [
    'BrainFuck',
    'FuckFuck',
    'Ook',
    'DNA#-line',
    'DNA#-helix',
    'C',
    'Python'
]

class FuckFuck:
    grammaire={
        'to_be_removed':[' '],
        'replace':[('f..k','fuck'),('s..g','shag'),('b..b','boob'),('t..s','tits'),('c..k','cock'),('k..b','knob'),('a..e','arse'),('b..t','butt')],
        'case_sentive':False,
        'regex_tokens':'((?:a..et..sb..t|f..k|s..g|b..b|t..s|c..k|k..b|a..e|b..t)!*)',
        'regex_group':'(a..et..sb..t|f..k|s..g|b..b|t..s|c..k|k..b|a..e|b..t)(!*)',
        'arsetitsbutt':'zero',
        'parse_arg':lambda cmd,arg:1+len(arg),
    }
    possible_translations=output_languages
    cmds ={'boob':'add',
        'tits':'sub',
        'fuck':'right',
        'shag':'left',
        'cock':'out',
        'knob':'read',
        'arse':'while_test',
        'butt':'while_end'}
    grammaire.update(cmds)
 
class Brainfuck:
    grammaire={
        'to_be_removed':[],
        'case_sentive':False,
        'replace':[],
        'regex_tokens':'(\[-\]|\.+|[,\[\]]|\++|-+|<+|>+)',
        'regex_group':'(\[-\]|[.,\[\]+-<>])([.+-><]*)',
        'parse_arg':lambda cmd,arg:1+len(arg),
    }
    cmds ={'+':'add',
        '-':'sub',
        '>':'right',
        '<':'left',
        '.':'out',
        ',':'read',
        '[':'while_test',
        ']':'while_end',
        '[-]':'zero',}
    grammaire.update(cmds)
    possible_translations=output_languages
    
class DNA:#DNA-sharp
    grammaire={
        'to_be_removed':[' ','-','\n'],
        'case_sentive':False,
        'replace':[],
        'regex_tokens':'(cgcgcgcgcgcg|(?:ta(?:at|gc|ta|cg)|cgat)(?:atat|atgc)*|(?:atta)+|(?:atcg)+|(?:atat)+|(?:atgc)+|gc(?:at|gc|ta|cg)|cg(?:gc|ta|cg))',
        'regex_group':'(cgcgcgcgcgcg|(?:at|gc|ta|cg)(?:at|gc|ta|cg))((?:(?:at|gc|ta|cg)(?:at|gc|ta|cg))*)',
        'parse_arg':lambda cmd,arg:(0 if arg=='' else (len(arg)//4)*(1 if arg.startswith('atat') else -1)) if re.match('(?:ta(?:at|gc|ta|cg)|cgat)',cmd) else 1+len(arg)//4,
    }
    cmds = {'atta':'add',
        'atcg':'sub',
        'atat':'right',
        'atgc':'left',
        'gcat':'out',
        'gcgc':'read',
        'gcta':'while_test',
        'gccg':'while_end',
        'taat':'dna_equal',
        'tagc':'dna_add',
        'tata':'dna_sub',
        'tacg':'dna_mult',
        'cgat':'dna_div',
        'cggc':'dna_oint',
        'cgta':'dna_iint',
        'cgcg':'nop',
        'cgcgcgcgcgcg':'quine'}
    grammaire.update(cmds)
    possible_translations=['Python','C']
class Ook:
    grammaire={
        'to_be_removed':[' '],
        'case_sentive':False,
        'replace':[],
        'regex_tokens':'(ook!ook\?ook!ook!ook\?ook!|ook.ook.)',
        'regex_group':'(ook!ook\?ook!ook!ook\?ook!|ook.ook.)(.*)',
        'parse_arg':lambda cmd,arg:1+len(arg),
    }
    cmds ={'ook.ook.':'add',
        'ook!ook!':'sub',
        'ook.ook?':'right',
        'ook?ook.':'left',
        'ook!ook.':'out',
        'ook.ook!':'read',
        'ook!ook?':'while_test',
        'ook?ook!':'while_end',
        'ook!ook?ook!ook!ook?ook!':'zero',}
    grammaire.update(cmds)
    possible_translations=output_languages
    
class Compiler:
    param={
        'values':{'min':0,'max':255},
        'tab_size':30000,
        'output_func':chr,
        'input_func':ord   
    }
     
    def __init__(self,language,param_arg={}):
        self.param.update(param_arg)
        self.init_python()
        self.language=language
    def parse(self,s):
        ir = []
        for c in self.language.grammaire['to_be_removed']:
            s=s.replace(c,'')
        if not self.language.grammaire['case_sentive']:
            s=s.lower()
        for pat,pat_rep in self.language.grammaire['replace']:
            s=re.sub(pat,pat_rep,s)
            
        for tok in re.findall(self.language.grammaire['regex_tokens'],s):
            cmd,arg = re.search(self.language.grammaire['regex_group'],tok).groups()
            #print(self.language.grammaire[cmd],cmd,arg)
            ir.append((self.language.grammaire[cmd],self.language.grammaire['parse_arg'](cmd,arg)))
        return ir
    def init_python(self):
        self.default_python={
#            'add':"tab[ptr] = (tab[ptr]+{}) % {}\n".format('{}',self.param['values']['max']),
#            'sub':"tab[ptr] = (tab[ptr]-{}) % {}\n".format('{}',self.param['values']['max']),
#            'right':"ptr = (ptr+{}) % {}\n".format('{}',self.param['tab_size']),
#            'left':"ptr = (ptr-{}) % {}\n".format('{}',self.param['tab_size']),
            'add':"tab[ptr] += {}\n",
            'sub':"tab[ptr] -= {}\n",
            'right':"ptr += {} \n",
            'left':"ptr -= {}\n",
            'out':"print(chr(tab[ptr])*{},end='')\n",
            'read':"tab[ptr] = ord(getch())\n",
            'while_test':"while tab[ptr]:\n",
            'while_end':"\n",
            'zero':"tab[ptr]=0\n",
            'start':"ptr,tab,s=0,[0]*{},''\n".format(self.param['tab_size']),
            'end':'',
            'branch_level':0,
            'dna_equal':"tab[ptr]=tab[ptr+{}]\n",
            'dna_add':"tab[ptr]+=tab[ptr+{}]\n",
            'dna_sub':"tab[ptr]-=tab[ptr+{}]\n",
            'dna_mult':"tab[ptr]*=tab[ptr+{}]\n",
            'dna_div':"tab[ptr]//=tab[ptr+{}]\n",
            'dna_iint':"tab[ptr] = ord(getch())-ord('0')\n",
            'dna_oint':"print(str(tab[ptr]),end='')\n",
            'nop':"\n",
            'quine':"print(source)\n",
        }
        self.eval_python=dict(self.default_python)
        self.eval_python['out']="s+=chr(tab[ptr])*{}\n"
        self.eval_python['branch_level']=1
        self.eval_python['start']="def fuck_prog():\n  "+self.eval_python['start']
        self.eval_python['end']="  return s\n"
     
        self.default_c={
            'add'   :"*ptr+={};\n",
            'sub'   :"*ptr-={};\n",
            'right' :"ptr +={};\n",
            'left'  :"ptr -={};\n",
            'out'   :"for(int i=0;i<{};i++)putchar(*ptr);\n",
            'read'  :"*ptr=getchar();\n",
            'while_test'    :"while (*ptr) {\n",
            'while_end'     :"}\n",
            'zero'  :"*ptr=0;\n",
            'start' :"main(){\n"+"  char* tab[{}]={};\n  char *ptr=tab;\n".format(self.param['tab_size'],'{0}'),
            'end'   :'}',
            'branch_level':1,
            'dna_equal':"*ptr=*(ptr+{});\n",
            'dna_add':"*ptr+=*(ptr+{});\n",
            'dna_sub':"*ptr-=*(ptr+{});\n",
            'dna_mult':"*ptr*=*(ptr+{});\n",
            'dna_div':"*ptr/=*(ptr+{});\n",
            'dna_iint':"*ptr = getchar()-'0';\n",
            'dna_oint':"""printf("%d",*ptr);\n""",
            'nop':"\n",
            'quine':"""printf("{}");\n""",
        }
    def driver(self,ir,instruction,source=''):
        branch_level= instruction['branch_level'] if 'branch_level' in instruction else 0
        prog = instruction['start']
        for i,arg in ir:
            prog += ' '*(branch_level*2)
            if i == 'quine':
                prog += instruction[i].format(source)
                continue
            if re.search('{}',instruction[i]):
                prog += instruction[i].format(arg)
            else:
                prog += instruction[i]
            if i == 'while_test':branch_level+=1
            if i == 'while_end':branch_level-=1

        prog += instruction['end']
        return prog
        
    def dna_sharp_driver(self,ir,form='helix',source=None):
        source='' if source is None else source
        dna={j:i for i,j in DNA.cmds.items()}
        dna['zero']=dna['while_test']+dna['sub']+dna['while_end']
        for cmd,arg in ir:
            if cmd in ['add', 'sub', 'right', 'left', 'out']:
                source += dna[cmd]*arg
            elif cmd in ['dna_equal', 'dna_add', 'dna_sub', 'dna_mult', 'dna_div'] and arg != 0:
                source += dna[cmd] + abs(arg)*('atat' if arg>0 else 'atgc')
            else:
                source += dna[cmd]
        helix=[
            "    {}{}\n",
            "   {}--{}\n",
            "  {}----{}\n",
            "  {}-----{}\n",
            "  {}-----{}\n",
            "  {}----{}\n",
            "   {}--{}\n"
            ]
        source = source.upper()
        if form=='helix':
            helix_s = ''
            ptr=0
            for i,j in zip(source[::2],source[1::2]):
                helix_s+=helix[ptr].format(i,j)
                ptr=(ptr+1)%len(helix)
            return helix_s
        if form=='line':
            return source
 
    def brainfuck_driver(self,ir):
        source=''
        translate = {j:i for i,j in Brainfuck.cmds.items()}
        for cmd,arg in ir:
            source+=translate[cmd]*arg
        return source
        
    def Ook_driver(self,ir):
        source=''
        translate = {j:i for i,j in Ook.cmds.items()}
        for cmd,arg in ir:
            source+=" ".join(re.findall('ook.',translate[cmd]*arg))+' '
        return source.title()
        
    def fuckfuck_driver(self,ir):
        source=''
        translate = {j:i for i,j in FuckFuck.cmds.items()}
        for cmd,arg in ir:
            if cmd in ['add', 'sub', 'right', 'left', 'out']:
                source += translate[cmd]+'!'*(arg-1)+' '
            else:
                source += translate[cmd]+' '
        return source.title()


if __name__=='__main__':
 
    parser = argparse.ArgumentParser(description='')
    input_languages = {
        'BrainFuck':Brainfuck(),
        'FuckFuck':FuckFuck(),
        'DNA#':DNA(),
        'Ook':Ook(),
    }

    
    parser.add_argument('-il','--input_language',default='auto',choices=list(input_languages.keys()),
        help="Set the language of the input. By default it is automatically recognized from the input file's extention")
    parser.add_argument('-ol','--output_language',default='Python',choices=output_languages,
        help='Set the language of the output. Default is %(default)s.')
    parser.add_argument('-i','--input',default='stdin',help='Set the input file. Default is %(default)s.')
    parser.add_argument('-o','--output',default='stdout',help='Set the output file. Default is %(default)s.')
    parser.add_argument('-r','--run',action='store_true',default=False,help='Run the input program')
    parser.add_argument('-c','--compile',action='store_true',default=False,help='Compile the input program into the output language')
    parser.add_argument('-w','--warnings',action='store_true',default=False,help='Print some warnings')
     
    parser.add_argument('--wrap',type=int,default=False,help='Set the wrapping parameter')
    parser.add_argument('--tab_size',type=int,default=30000,help='Set the array size. Default is 30000')
    
    args = parser.parse_args(sys.argv[1:])
    #print(args)
    text=''
    if args.input == 'stdin':
        text=sys.stdin.read() 
    elif os.path.isfile(args.input):
        with open(args.input,'r') as f: 
            text=f.read()
    else:
        print('file {} not found'.format(args.input))
        exit(1)
    
    #print(text)
    if args.output != 'stdout':
        sys.stdout = open(args.output,'w')
 
    if args.input_language == 'auto' :
        if args.input != 'stdin':
            for reg,lang in zip(['.*\.bf','.*\.ff','.*\.ook','.*\.dna'],['BrainFuck','FuckFuck','Ook','DNA#']):
                if re.match(reg,args.input):
                    language = lang
        else:
            language = 'BrainFuck'
    else:
        language=args.input_language
    if language not in input_languages:
        print('language {} not supported or ill writen'.format(language))
        exit(1)
    if args.warnings:print('language set to {}. Use argument -il to change that.'.format(language),file=sys.stderr)
    
    compiler = Compiler(input_languages[language])
    ir = compiler.parse(text)
    python_source=compiler.driver(ir,compiler.default_python)
    if args.run:
        exec(python_source)
    if args.compile:
        if args.output_language not in input_languages[language].possible_translations:
            print('Output language {} not supported for input language {}'.format(args.output_language,language))
            exit(1)
        source_output={
                'BrainFuck':lambda ir:compiler.brainfuck_driver(ir),
                'FuckFuck':lambda ir:compiler.fuckfuck_driver(ir),
                'Ook':lambda ir:compiler.Ook_driver(ir),
                'DNA#-line':lambda ir:compiler.dna_sharp_driver(ir,form='line'),
                'DNA#-helix':lambda ir:compiler.dna_sharp_driver(ir,form='helix'),
                'C':lambda ir:compiler.driver(ir,compiler.default_c),
                'Python':lambda ir:compiler.driver(ir,compiler.default_python)}[args.output_language](ir)
        
        print(source_output,end='')
    
    if args.output != 'stdout':
        sys.stdout.close()