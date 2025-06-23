if "blowjob" in prompt.lower() or "bl0wj0b" in prompt.lower() or "deepthroat" in prompt.lower():
      print("Setting bj adapter", flush=True)
      self.pipe.set_adapters(["bj"], adapter_weights=[0.7])
      prompt = "bl0wj0b, blowjob, deepthroat. a sexy woman. " + prompt
    elif "blow job" in prompt.lower():
      print("Setting bj2 adapter", flush=True)
      self.pipe.set_adapters(["bj2"], adapter_weights=[0.7])
    elif "titfuck" in prompt.lower():
      print("Setting titfuck adapter", flush=True)
      self.pipe.set_adapters(["tf"], adapter_weights=[0.7])
      prompt = "A woman titfucks a man. She moves her body up and down slowly and seductively. " + prompt
    elif "masturbation" in prompt.lower() or "rubbing" in prompt.lower():
      print("Setting masturbation adapter", flush=True)
      self.pipe.set_adapters(["masturbation"], adapter_weights=[0.7])
      prompt = "A woman masturbates herself. She is rubbing her vagina with her fingers. She moves her body up and down slowly and seductively." + prompt
    elif "doggy" in prompt.lower():
      print("Setting doggy adapter", flush=True)
      self.pipe.set_adapters(["doggy"], adapter_weights=[0.7])
      prompt = "POVdog. A POV video showing a man having sex doggy style sex with a woman." + prompt
    elif "cum" in prompt.lower():
      print("Setting cumshot adapter", flush=True)
      self.pipe.set_adapters(["cumshot"], adapter_weights=[0.7])
      prompt = "Cum shoots from off screen" + prompt
    elif "anal" in prompt.lower():
      print("Setting anal adapter", flush=True)
      self.pipe.set_adapters(["anal"], adapter_weights=[0.7])
      prompt = "She moves up and down on top of him as his penis penetrates her asshole." + prompt
    else:
      print("Setting bj adapter", flush=True)
      self.pipe.set_adapters(["bj"], adapter_weights=[0.7])
      prompt = "bl0wj0b, blowjob, deepthroat. a sexy woman. " + prompt