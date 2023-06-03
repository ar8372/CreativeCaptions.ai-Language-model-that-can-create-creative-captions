from modules import * 



model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def predict_step(images_):
  images = []
  for image_ in images_:
    i_image = image_
    if i_image.mode != "RGB":
      i_image = i_image.convert(mode="RGB")

    images.append(i_image)

  pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device)

  output_ids = model.generate(pixel_values, **gen_kwargs)

  preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]


  preds1 = make_creative(preds[0],64,3)
  return [preds[0]] + preds1


# HElper Function
def choose_from_top(probs, n=5):
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)

## Start Creative Captioning
class config:
    Tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')

# Model Loading
model_inst = GPT2LMHeadModel.from_pretrained('gpt2-medium')
special_tokens_dict = {'pad_token': '<PAD>','bos_token':'<soq>','sep_token':'<eoq>'}
num_added_toks = config.Tokenizer.add_special_tokens(special_tokens_dict)
print('We have added', num_added_toks, 'tokens')
model_inst.resize_token_embeddings(len(config.Tokenizer))

#loading Model state
models_path = "models_folder\gpt2_medium_joke_insta.pt"
#model.load_state_dict(torch.load(models_path, map_location=torch.device('cpu')))
model_inst.load_state_dict(torch.load(models_path, map_location=torch.device('cpu')))

model_inst.to(device)

def make_creative(start_of_joke,length_of_joke=96,number_of_jokes=2):
    joke_num = 0
    model_inst.eval()
    all_jokes = []
    with torch.no_grad():
        for joke_idx in range(number_of_jokes):
        
            joke_finished = False

            cur_ids = torch.tensor(config.Tokenizer.encode(start_of_joke)).unsqueeze(0).to(device)

            for i in range(length_of_joke):
                outputs = model_inst(cur_ids, labels=cur_ids)
                loss, logits = outputs[:2]
                softmax_logits = torch.softmax(logits[0,-1], dim=0) #Take the first(from only one in this case) batch and the last predicted embedding
                if i < 3:
                    n = 20
                else:
                    n = 3
                next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=n) #Randomly(from the topN probability distribution) select the next word
                cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device) * next_token_id], dim = 1) # Add the last word to the running sequence

                if next_token_id in config.Tokenizer.encode('<|endoftext|>'):
                    joke_finished = True
                    break

            
            if joke_finished:
                
                joke_num = joke_num + 1
                
                output_list = list(cur_ids.squeeze().to('cpu').numpy())
                output_text = config.Tokenizer.decode(output_list)

                #print(output_text+'\n')
                all_jokes.append(output_text)
        
    return all_jokes

# # Start Predicting
# predict("How do you feel",64,1)

def clean_text(st):
    # 'a man kicking a soccer ball on a field <PAD> a man kicking a soccer ball on a field <|endoftext|>'
    st=st.split("<eoq>")[-1]
    for k,j in enumerate([" ", ""]):
        for i in ["<soq>", "<eoq>" , "<|endoftext|>", "<PAD>"]:
            if k ==0:
                st= st.replace(j+i+j, " ")
            else:
                st= st.replace(j+i+j, "")

    return st.strip()


if __name__ == "__main__":
    path = sys.argv[1]
    img = Image.open(path)
    result = predict_step([img])
    result = [clean_text(st) for st in result]
    for r in result:
        print(r)