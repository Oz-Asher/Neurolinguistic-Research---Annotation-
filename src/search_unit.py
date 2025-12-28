from .csv_class import CSV



def find_sentences(name, inserted_unit):

    # These are the boundaries that don't require us to mention that they exist
    simple_boundaries = [0,1]

    # These are boundaries that cut off the sentences
    end_boundaries = [1]

 
    boundary = CSV(name).rows('boundary')
    words = CSV(name).rows('word')


    inserted_unit = inserted_unit.split()

    # Find all of the indexes of inserted_word in words
    indexes = [
        i for i in range(len(words) - len(inserted_unit) + 1)
        if [w.lower() for w in words[i:i+len(inserted_unit)]] == [w.lower() for w in inserted_unit]
    ] 
    

    sentences = {}
    for index in indexes:

        # Look backwards for sentence start
        num = 0
        first_part = ''
        for word in words[index::-1]:
            first_part = first_part + ' ' + word
            
            if float(boundary[index-num]) not in simple_boundaries: # If the word has a unique boundary - mark it.
                first_part = first_part + f'({int(float(boundary[index-num]))})'

            num = num + 1
            if float(boundary[index-num]) in end_boundaries:
                first_part = (' '.join(first_part.split()[::-1][:-1])).strip()
                break 
        
        start_index = CSV(name).rows('index')[index-num+1] # Finding the start index in the excel

        # Look forward for sentence end
        num = 0
        last_part = ''
        if float(boundary[index]) not in end_boundaries:
            for word in words[index:]:
                last_part = last_part + ' ' + word

                if float(boundary[index+num]) not in simple_boundaries: # If the word has a unique boundary - mark it.
                    last_part = last_part + f'({int(float(boundary[index+num]))})'
                 
                num = num + 1
                if index+num < len(boundary) and float(boundary[index+num]) in end_boundaries:
                    last_part = (last_part + ' ' +  words[index+num]).strip()

                    if float(boundary[index+num]) not in simple_boundaries: # If the last word has a unique boundary - mark it.
                        last_part = last_part + f'({int(float(boundary[index+num]))})'
                    break
        else:
            last_part = words[index]
            if float(boundary[index]) not in simple_boundaries: # If the word has a unique boundary - mark it.
                last_part = last_part + f'({int(float(boundary[index]))})'

        end_index = CSV(name).rows('index')[index+num] # Finding the end index in the excel


        sentence = (first_part + ' ' + last_part).strip()
        if sentence not in list(sentences.values()):
            if len(sentence.split()) > 1:
                sentences[f'{start_index}-{end_index}'] = sentence
            else:
                sentences[CSV(name).rows('index')[index]] = sentence


    return sentences


def search(name):
    
    while True:

        inserted_unit = input(f'\nSearch for unit in the excel {name}: ')

        if inserted_unit == '/end/': # Break the loop
            break
        
        sentences = find_sentences(name, inserted_unit)

        print(f'\n"{inserted_unit}" was found in {len(sentences)} sentences in the excel of {name}:')
        for index, sentence in sentences.items():
            print(f"{index}: {sentence}")
   

