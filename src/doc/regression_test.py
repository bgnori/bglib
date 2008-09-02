#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim: syntax=python
#
# Copyright 2006-2008 Noriyuki Hosaka nori@backgammon.gr.jp
#
import unittest
import bglib.doc.mock
import bglib.doc.bgwiki
import bglib.doc.html

class FormatterTest(unittest.TestCase):
  def setUp(self):
    db = bglib.doc.mock.DataBaseMock()
    macroprocessor = bglib.doc.macro.Processor(db)
    self.wiki = bglib.doc.bgwiki.Formatter(db)

  def test_1(self):
    self.wiki.parse('''http:|http:\'`_8\n7h#5#_[match:[>8!h=_*`6aquery:`[!match:wiki:27c._entry:hv.00||match:+d"+" #..7::vquery:"\n5https:entry:\'1https:~8c\n`|ha`}:1f\':hvhttps:4`https:=<7\n] f93=/CamelWord9479{+||ventry:i1`<!1 b\n7b entry:match:<1wiki:https:!g-CamelWord>\n||>4+ch .>g+`CamelWord4=:v>::||entry::+>ce :wiki:e2>.hifehttp:""b}`">7f2dhCamelWordentry:-match:0entry:}d"3a.+e~9v||:v\'7||_&1<[+CamelWord[.centry:v0.|dd30match:fwiki:\n-*vdv[5wiki:{[0\'4|4=`||}#vhttps:!\'query:[CamelWordev{|b"bhttps:`_]c=3!f}dd]aCamelWord+{_>""\n>>a0v|b^_}7^73match:" c7chttps:5||]7g=4g3{}.">wiki:0+[]&[\'\'4:}http:ig589match:64{wiki:=< -CamelWord~~!c|=5{c-3`=>imatch:dv^match:_ e<query:||wiki:9[*^8f^]||&+*-~||~\n{:a}#+match:>388https:0e5.*3#f{|`{924:3_86/http:e_||\n!c.22<0bCamelWord0*bi~.d"+wiki:=c&#:2g"&CamelWord<-*: b&49c~`||! =entry:2match:||_#8hmatch:http:i^ghe1query:15|6b0^~#ahttps:d`eca0 +!+match::"`query:3c19|wiki:de=\'}https:egdhttps:|3https:http:e+6e1i.ii6e_^|eCamelWord=1=c]a||!7{/{4h~[9{:v5[g+53>+[7*+ientry:\n2entry:f&vCamelWord8||http:match:3+4||wiki:/v*.{|]|vhttp:f>||bCamelWord{!v]\'1<&wiki:v`entry:e}6wiki:|cc]f cb2&*]}h11|3364query:http:9`23.7||[&entry:CamelWord"#~https:/#_/entry:}*CamelWord5#wiki:wiki:https:\n23#.~1d7!_8]]-\n9\'https:3|dentry:7\n\n[/` #d1_.a1&~CamelWordg-#https:e418aac*~v-entry:"f_dwiki:ag1\'dquery:]_&~&]e-http:2-8`8_[wiki:==fmatch:match:ec*\nf|||c&}8.1{:/`h6*ghttp:query:<3+f.+g#bvivh8https:\'~c1~CamelWordhttps: 3entry:-9:^9_:8:http:24.dwiki:`!&+]9c\'match:>/.:g CamelWorddCamelWordv.:8~76\n\'>https:^0wiki:v8^9fhCamelWorde0}_&/h35wiki:dquery:^9}!wiki:http:http:{<query:[match:\n96c b9`wiki:8hwiki:..hentry:CamelWordentry:d}=`^+entry:4wiki:v>0+9]/cgwiki:`=9[f1vhttp:f{&vimatch:!!=` vh48c-+|-|||>entry:=v0.wiki:6!2h09i9c5e||ve85^+-9>`0'''    )

  def test_2(self):
    self.wiki.parse('7![f=.query:&4.[query:http:entry:c-a^query: _b!*a28query:http::http:4"7match:gg6 7}=ii8wiki:match:wiki:!-`!~b=`&2h_^9\n{cde&f}https:_7=query: "2bc2}"=}#6i8i.f&<\n3~_/a\nv:]+{5h+_/def\n4f5match:>4[5=! h&-4match:714\n`6!5id}+/3.`{}+entry::]:a}*query:i\nentry:e^ \'fhe*if<\n<*/99{{match:^:https:!806~&=/`+ |https:wiki:<e&*http:[|c75he[!v]http:g\n[i<>&8|-*3-[|&f5<query:5v+gfb9[cv55/bev=wiki:!\n-query:\'9|\'+~https:"wiki:#>~https:`\nd\n  d >2hwiki:\'|https:v714query:c\'*https:*8/+ \n')

  def test_3(self):
    self.wiki.parse(':1.]http:c0d8~{#"i"entry:<3~[1{/`fh4`90v^8]g4[c#&f="_*3[h\n+CamelWord_>72http:97"CamelWord|bhttps:b]CamelWord5CamelWorddh}=2_a[c9https:d+1^match:5 a1CamelWordfbh[}\'\'\'*6_query:"match:34{" ||hmatch:cg<wiki:985/+>8b-0{\'i-61http:.>^~+.>230]\n5:7/entry:-ahttps:[~}9CamelWord"}9=^||i#6a{<*.-:[7https:.{>https:~6d:&:]match:d <0&2http:4\n}+wiki:5b[ entry::+/||0`g}#^|g<*h||0adhquery:_+="-[:`match::/5||\n}0CamelWord||e*!query:wiki:fg5-afg7/{i-wiki:5`\'b[/b0+.fh5a<CamelWord.=4d\'\n  8 .*[h3cf7.|_>')

  def test_3_1(self):
    self.wiki.parse(':1.]http:c0d8~{#"i"entry:<3~[1{/`fh4`90v^8]g4[c#&f="_*3[h\n+CamelWord_>72http:97"CamelWord|bhttps:b]CamelWord5CamelWorddh}=2_a[c9https:d+1^match:5 a1CamelWordfbh[}\'\'\'*6_query:"match:34{" ||hmatch:cg<wiki:985/+>8b-0{\'i-61http:.>^~+.>230]\n')

  def test_3_2(self):
    self.wiki.parse('5:7/entry:-ahttps:[~}9CamelWord"}9=^||i#6a{<*.-:[7https:.{>https:~6d:&:]match:d <0&2http:4\n}+wiki:5b[ entry::+/||0`g}#^|g<*h||0adhquery:_+="-[:`match::/5||\n}0CamelWord||e*!query:wiki:fg5-afg7/{i-wiki:5`\'b[/b0+.fh5a<CamelWord.=4d\'\n  8 .*[h3cf7.|_>')


  def test_3_2_1(self):
    self.wiki.parse('5:7/entry:-ahttps:[~}9CamelWord"}9=^||i#6a{<*.-:[7https:.{>https:~6d:&:]match:d <0&2http:4\n}+wiki:5b[ entry::+/||0`g}#^|g<*h||0adhquery:_+="-[:`match::/5||\n')

  def test_3_2_2(self):
    self.wiki.parse('}0CamelWord||e*!query:wiki:fg5-afg7/{i-wiki:5`\'b[/b0+.fh5a<CamelWord.=4d\'\n  8 .*[h3cf7.|_>')

  def test_3_2_2_1(self):
    self.wiki.parse('}0CamelWord||e*!query:wiki:fg5-afg7/{i-wiki:5`\'b[/b0+.fh5a<CamelWord.=4d\'')

  def test_3_2_2_2(self):
    self.wiki.parse('  8 .*[h3cf7.|_>')

  def test_bad_indent(self):
    self.wiki.parse('  8 ')


