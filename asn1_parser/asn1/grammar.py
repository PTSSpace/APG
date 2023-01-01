GRAMMAR = """
Asn1Module:
  'Module-'module_name=NameLower
    'DEFINITIONS AUTOMATIC TAGS ::= BEGIN'(comment=Asn1Comment)?
    ('IMPORTS' import_items+=ImportItem ';' (comment_import=Asn1Comment)?)?
    definitions+=Definitions
  'END'
;

ImportItem:
  definitions+=NameCapital[',']
  'FROM Module-'module_name=NameLower
  (comment=Asn1Comment)?
;

Asn1Comment[noskipws]:
  (' ')*
  '--'
  (' ')*
  is_little_endian?='ENDIANNESS(LITTLE)'
  (' ')*
  ('[' unit=/[%A-Za-z\\d\\/\\^]+/ ']')?
  (' ')*
  (comment=/[A-Za-z0-9\\*\\(\\)\\.\\/%:, -_]+$/)?
;

NameLower:
  /[a-z][a-z\\d]*(-[a-z\\d]+)*/
;

NameCapital:
  /[A-Z][a-z\\d]*(-[a-z\\d]+)*/
;

Definitions:
  Choice | Enumerated | Sequence | SimpleDefinition
;

Enumerated:
  type_name=NameCapital '::= ENUMERATED {'(comment=Asn1Comment)?
    (enum=EnumeratedItemNotLast)*
    enum=EnumeratedItemLast
  '}'
;

EnumeratedItemNotLast:
  key=NameLower ('('pos=INT')')? (',') (comment=Asn1Comment)?
;

EnumeratedItemLast:
  key=NameLower ('('pos=INT')')? (comment=Asn1Comment)?
;

Asn1Type[noskipws]:
  ' 'type_name='REAL'('('begin=STRICTFLOAT' .. 'end=STRICTFLOAT')')? |
  ' 'type_name='INTEGER'('('begin=INT'..'end=INT')')? |
  ' 'type_name='NULL' |
  ' 'type_name='BOOLEAN' |
  ' 'type_name=Asn1String |
  ' 'type_name=Array |
  ' 'type_name=NameCapital // TODO: correct to match exactly a defined typ
;

KeyTypePairNotLast:
  (
    key=NameLower
    asn_type=Asn1Type
    ','
    (comment=Asn1Comment)?
  ) | (
    key=NameLower
    asn_type=Asn1Type
    (comment=Asn1Comment)?
    with_components=WithComponents
    ','
  )
;

KeyTypePairLast:
  (
    key=NameLower
    asn_type=Asn1Type
    (comment=Asn1Comment)?
    (with_components=WithComponents)?
  )
;

WithComponents:
  '(WITH COMPONENTS {' (comment=Asn1Comment)?
    (components=ComponentsItemNotLast)*
    components=ComponentsItemLast
  '})'
;

ComponentsItemNotLast:
  key=NameLower (
    '(' value=INT ')' |
    '(' value=STRICTFLOAT ')' |
    '(' value='TRUE' ')' |
    '(' value='FALSE' ')' |
    value=WithComponents
  ) (',') (comment=Asn1Comment)?
;

ComponentsItemLast:
  key=NameLower (
    '(' value=INT ')' |
    '(' value=STRICTFLOAT ')' |
    '(' value='TRUE' ')' |
    '(' value='FALSE' ')' |
    value=WithComponents
  ) (comment=Asn1Comment)?
;

Choice:
  type_name=NameCapital '::= CHOICE {'(comment=Asn1Comment)?
    (choice=KeyTypePairNotLast)*
    choice=KeyTypePairLast
  '}'
;

Sequence:
  type_name=NameCapital '::= SEQUENCE {'(comment=Asn1Comment)?
    (seq=KeyTypePairNotLast)*
    seq=KeyTypePairLast
  '}'
;

SimpleDefinition:
  type_name=NameCapital '::=' asn_type=Asn1Type (comment=Asn1Comment)?
;

Array:
  'SEQUENCE (SIZE ('length=INT')) OF' asn_type=Asn1Type
;
// TODO check whether SEQUENCE OF SEQUENCE OF ... is allowed in ASN.1

Asn1String:
  (type_name='IA5String' | type_name='NumericString')
  ' (SIZE ('length=INT'))'
;
"""
