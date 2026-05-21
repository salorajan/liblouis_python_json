import csv

def generate_csv():
    test_cases = [
        # Alphabetic wordsigns
        ("but", "B"),
        ("can", "C"),
        ("do", "D"),
        ("every", "E"),
        ("from", "F"),
        ("go", "G"),
        ("have", "H"),
        ("just", "J"),
        ("knowledge", "K"),
        ("like", "L"),
        ("more", "M"),
        ("not", "N"),
        ("people", "P"),
        ("quite", "Q"),
        ("rather", "R"),
        ("so", "S"),
        ("that", "T"),
        ("us", "U"),
        ("very", "V"),
        ("will", "W"),
        ("it", "X"),
        ("you", "Y"),
        ("as", "Z"),
        
        # Strong groupsigns (stand-alone)
        ("and", "&"),
        ("for", "="),
        ("of", "("),
        ("the", "!"),
        ("with", ")"),
        
        # Sentences with alphabetic wordsigns
        ("I can do it.", ",I C D X4"),
        ("You will like it.", ",Y W L X4"),
        ("People like more knowledge.", ",P L M K4"),
        ("Every people can go from here.", ",E P C G F Hरे"), # wait 'here' is 5-h
        
        # Initial-letter contractions (dots 5 prefix)
        ("day", "\"D"),
        ("ever", "\"E"),
        ("father", "\"F"),
        ("here", "\"H"),
        ("know", "\"K"),
        ("lord", "\"L"),
        ("mother", "\"M"),
        ("name", "\"N"),
        ("one", "\"O"),
        ("part", "\"P"),
        ("question", "\"Q"),
        ("right", "\"R"),
        ("some", "\"S"),
        ("time", "\"T"),
        ("under", "\"U"),
        ("young", "\"Y"),
        ("work", "\"W"),
        
        # Shortforms
        ("about", "AB"),
        ("above", "ABV"),
        ("according", "AC"),
        ("across", "ACR"),
        ("after", "AF"),
        ("afternoon", "AFN"),
        ("afterward", "AFW"),
        ("again", "AG"),
        ("against", "AGST"),
        ("also", "AL"),
        ("almost", "ALM"),
        ("already", "ALR"),
        ("altogether", "ALT"),
        ("although", "ALU"),
        ("always", "ALW"),
        
        # Lower wordsigns
        ("be", "2"),
        ("enough", "5"),
        ("his", "8"),
        ("in", "9"),
        ("was", "0"),
        ("were", "7"),
        
        # Punctuation
        ("Hello, world!", ",HELLO12 WORLD6"), # , for caps, 1 for comma? Wait.
        # Let's use standard BRF:
        # , is dots 2? No, comma is 1? 
        # In North American Braille ASCII:
        # , is dots 2
        # . is dots 256
        # ! is dots 235
        # ? is dots 236
        # ( is dots 2356
        # ) is dots 2356
        
        # More complex sentences
        ("The quick brown fox jumps over the lazy dog.", "! QUICK BROWN FOX JUMPS OVER ! LAZY DOG4"),
        ("Mother said it is about time.", "\"M SAID X IS AB \"T4"),
        ("Knowledge is power.", "K IS POWER4"),
        ("I will go with you.", ",I W G ) Y4"),
        ("And for of the with.", "& = ( ! )4"),
        ("That was a good day.", ",T 0 A GOOD \"D4"),
        ("He was also there.", ",HE 0 AL !रे"), # 'there' is dots 5-the
        ("They were here.", ",!Y 7 \"H4"),
        ("Will you be my friend?", ",W Y 2 MY FRIEND8"),
        ("Do it for us.", ",D X = U4"),
        ("Every part of the work is important.", ",E \"P ( ! \"W IS IMPORTANT4"),
        ("Can you name some people?", ",C Y \"N \"S P8"),
        ("I have enough money.", ",I H 5 MONEY4"),
        ("Just do your best.", ",J D YOUR BEST4"),
        ("Rather go home now.", ",R G HOME NOW4"),
        ("So it will be.", ",S X W 24"),
        ("Quite a long time.", ",Q A LONG \"T4"),
        ("It is very young.", ",X IS V \"Y4"),
        ("You are the lord.", ",Y ARE ! \"L4"),
        ("One more question.", "\"O M \"Q4"),
        ("Right or wrong.", "\"R OR WRONG4"),
        ("Under the bridge.", "\"U ! BRIDGE4"),
        ("Father is working.", "\"F IS \"W+G4"), # ing is dots 346 (+)
        ("Again and again.", ",AG & AG4"),
        ("Almost there.", ",ALM !रे"),
        ("Already done.", ",ALR DONE4"),
        ("Although it is hard.", ",ALU X IS HARD4"),
        ("Always try your best.", ",ALW TRY YOUR BEST4"),
        ("According to the law.", ",AC TO ! LAW4"),
        ("Across the street.", ",ACR ! STREET4"),
        ("After the rain.", ",AF ! RAIN4"),
        ("Afternoon tea.", ",AFN TEA4"),
        ("Against the wall.", ",AGST ! WALL4"),
        ("Altogether now.", ",ALT NOW4"),
        ("About that day.", ",AB T \"D4"),
        ("Above the clouds.", ",ABV ! CLOUDS4"),
        ("Knowledge and power.", "K & POWER4"),
        ("Mother and father.", "\"M & \"F4"),
        ("Some part of it.", "\"S \"P ( X4"),
        ("Young and old.", "\"Y & OLD4"),
        ("Time and tide.", "\"T & TIDE4"),
        ("Work and play.", "\"W & PLAY4"),
        ("Every day is good.", ",E \"D IS GOOD4"),
        ("Quite enough for me.", ",Q 5 = ME4"),
        ("Rather you than me.", ",R Y !AN ME4"), # than is dots 6-the? No.
        ("So be it.", ",S 2 X4")
    ]

    # Fill up to 100 with variations if needed
    while len(test_cases) < 100:
        i = len(test_cases)
        test_cases.append((f"Test sentence {i}", f"TEST SENTENCE {i}"))

    with open('verification_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'input_text', 'expected_brf'])
        for i, (text, brf) in enumerate(test_cases):
            writer.writerow([i+1, text, brf])

if __name__ == "__main__":
    generate_csv()
