
from platform import window
self = __import__(__name__)

window.eval("""
window.rsplit1 = function (sep, maxsplit) {
    var result = []
    console.log("rsplit1:", sep, maxsplit)
    if ( (sep === undefined) || (sep === null)  || (!sep) ) {
        sep = " "
    }

    if (maxsplit === 0  )
        return [window.strsrc]

    maxsplit = maxsplit || -1

    var data = window.strsrc.split(sep)


    if (!maxsplit || (maxsplit<0) || (data.length==maxsplit+1) )
        return data

    while (data.length && (result.length < maxsplit)) {
        result.push( data.pop() )
    }
    if (result.length) {
        result.reverse()
        if (data.length>1) {
            // thx @imkzh
            return [data.join(sep), ...result ]
        }
        return result
    }
    return [window.strsrc]
}

window.rsplit2 = function(sep, maxsplit) {
    var split = window.strsrc.split(sep);
    return maxsplit ? [ split.slice(0, -maxsplit).join(sep) ].concat(split.slice(-maxsplit)) : split;
}

""")



def checkequal(want, src, fn, sep = None, maxsplit = -1):
    test = src.rsplit(sep,maxsplit)
    if want != test:
        print(f"ERROR {want=} {test=} for",opts)

    head = False
    def header():
        nonlocal head
        print()
        print("_"*40)
        print(f'testing "{src}".rsplit({sep=},{maxsplit=})')
        head = True

    window.strsrc  = src
    test = list( map(str, window.rsplit1(sep,maxsplit) ))
    if want != test:
        if not head:
            header()
        print(f'ERROR 1 {want=} {test=} for "{src}".rsplit({sep=},{maxsplit=})')


    window.strsrc  = src
    test = list( map(str, window.rsplit2(sep,maxsplit) ))
    if want != test:
        if not head:
            header()
        print(f'ERROR 2 {want=} {test=} for "{src}".rsplit({sep=},{maxsplit=})')
        print()



async def main():
    # without arg
    self.checkequal(['a', 'b', 'c', 'd'], 'a b c d', 'rsplit')
    self.checkequal(['a', 'b', 'c', 'd'], 'a  b  c d', 'rsplit')
    self.checkequal([], '', 'rsplit')

    # by a char
    self.checkequal(['a', 'b', 'c', 'd'], 'a|b|c|d', 'rsplit', '|')
    self.checkequal(['a|b|c', 'd'], 'a|b|c|d', 'rsplit', '|', 1)
    self.checkequal(['a|b', 'c', 'd'], 'a|b|c|d', 'rsplit', '|', 2)
    self.checkequal(['a', 'b', 'c', 'd'], 'a|b|c|d', 'rsplit', '|', 3)
    self.checkequal(['a', 'b', 'c', 'd'], 'a|b|c|d', 'rsplit', '|', 4)
    self.checkequal(['a', 'b', 'c', 'd'], 'a|b|c|d', 'rsplit', '|', sys.maxsize-100)
    self.checkequal(['a|b|c|d'], 'a|b|c|d', 'rsplit', '|', 0)
    self.checkequal(['a||b||c', '', 'd'], 'a||b||c||d', 'rsplit', '|', 2)
    self.checkequal(['abcd'], 'abcd', 'rsplit', '|')
    self.checkequal([''], '', 'rsplit', '|')
    self.checkequal(['', ' begincase'], '| begincase', 'rsplit', '|')
    self.checkequal(['endcase ', ''], 'endcase |', 'rsplit', '|')
    self.checkequal(['', 'bothcase', ''], '|bothcase|', 'rsplit', '|')

    self.checkequal(['a\x00\x00b', 'c', 'd'], 'a\x00\x00b\x00c\x00d', 'rsplit', '\x00', 2)

    self.checkequal(['a']*20, ('a|'*20)[:-1], 'rsplit', '|')
    self.checkequal(['a|a|a|a|a']+['a']*15, ('a|'*20)[:-1], 'rsplit', '|', 15)

    # by string
    self.checkequal(['a', 'b', 'c', 'd'], 'a//b//c//d', 'rsplit', '//')
    self.checkequal(['a//b//c', 'd'], 'a//b//c//d', 'rsplit', '//', 1)
    self.checkequal(['a//b', 'c', 'd'], 'a//b//c//d', 'rsplit', '//', 2)
    self.checkequal(['a', 'b', 'c', 'd'], 'a//b//c//d', 'rsplit', '//', 3)
    self.checkequal(['a', 'b', 'c', 'd'], 'a//b//c//d', 'rsplit', '//', 4)
    self.checkequal(['a', 'b', 'c', 'd'], 'a//b//c//d', 'rsplit', '//', sys.maxsize-5)
    self.checkequal(['a//b//c//d'], 'a//b//c//d', 'rsplit', '//', 0)
    self.checkequal(['a////b////c', '', 'd'], 'a////b////c////d', 'rsplit', '//', 2)
    self.checkequal(['', ' begincase'], 'test begincase', 'rsplit', 'test')
    self.checkequal(['endcase ', ''], 'endcase test', 'rsplit', 'test')
    self.checkequal(['', ' bothcase ', ''], 'test bothcase test',
                    'rsplit', 'test')
    self.checkequal(['ab', 'c'], 'abbbc', 'rsplit', 'bb')
    self.checkequal(['', ''], 'aaa', 'rsplit', 'aaa')
    self.checkequal(['aaa'], 'aaa', 'rsplit', 'aaa', 0)
    self.checkequal(['ab', 'ab'], 'abbaab', 'rsplit', 'ba')
    self.checkequal(['aaaa'], 'aaaa', 'rsplit', 'aab')
    self.checkequal([''], '', 'rsplit', 'aaa')
    self.checkequal(['aa'], 'aa', 'rsplit', 'aaa')
    self.checkequal(['bbob', 'A'], 'bbobbbobbA', 'rsplit', 'bbobb')
    self.checkequal(['', 'B', 'A'], 'bbobbBbbobbA', 'rsplit', 'bbobb')

    self.checkequal(['a']*20, ('aBLAH'*20)[:-4], 'rsplit', 'BLAH')
    self.checkequal(['a']*20, ('aBLAH'*20)[:-4], 'rsplit', 'BLAH', 19)
    self.checkequal(['aBLAHa'] + ['a']*18, ('aBLAH'*20)[:-4],
                    'rsplit', 'BLAH', 18)

    # with keyword args
    self.checkequal(['a', 'b', 'c', 'd'], 'a|b|c|d', 'rsplit', sep='|')
    self.checkequal(['a', 'b', 'c', 'd'], 'a b c d', 'rsplit', sep=None)
    self.checkequal(['a b c', 'd'], 'a b c d', 'rsplit', sep=None, maxsplit=1)
    self.checkequal(['a|b|c', 'd'], 'a|b|c|d', 'rsplit', '|', maxsplit=1)
    self.checkequal(['a|b|c', 'd'],  'a|b|c|d', 'rsplit', sep='|', maxsplit=1)
    self.checkequal(['a|b|c', 'd'],  'a|b|c|d', 'rsplit', maxsplit=1, sep='|')
    self.checkequal(['a b c', 'd'], 'a b c d', 'rsplit', maxsplit=1)

    if 0:
        # argument type
        self.checkraises(TypeError, 'hello', 'rsplit', 42, 42, 42)

        # null case
        self.checkraises(ValueError, 'hello', 'rsplit', '')
        self.checkraises(ValueError, 'hello', 'rsplit', '', 0)

asyncio.run(main())

