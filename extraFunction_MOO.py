def create_spine(sim, icell, sec, seg, number=0, neck_diam=0.25, neck_length=1.35,
                 head_diam=0.944,passive_val={}):  # np.sqrt(2.8/(4*np.pi))
    neck = sim.neuron.h.Section(name="spineNeck" + str(number))
    head = sim.neuron.h.Section(name="spineHead" + str(number))
    # icell.add_sec(neck)#?# moria why add twice??
    # icell.add_sec(head)
    neck.L = neck_length
    neck.diam = neck_diam
    head.L = head.diam = head_diam
    head.connect(neck(1))
    neck.connect(sec(seg))
    sim.neuron.h("access " + str(neck.hoc_internal_name()))
    try: icell.add_sec(neck)
    except:
        icell.all.append(neck)
        if sec.name().find('apic') > -1:
            icell.apical.append(neck)
        else:
            icell.basal.append(neck)
    # if sec.name().find('dend') > -1: #?# moria- need to be sure it is ok to remove the neck and head from the dend list
    #     icell.dend.append(neck)
    # else:
    #     icell.apical.append(neck)
    sim.neuron.h.pop_section()
    sim.neuron.h("access " + str(head.hoc_internal_name()))
    try:icell.add_sec(head) #if using in hoc or ASC file (load_hoc,load_ASC
    except:
        icell.all.append(head) #if using in swc
        if sec.name().find('apic') > -1:
            icell.apical.append(head)
        else:
            icell.basal.append(head)
    # if sec.name().find('dend') > -1: #?# moria- need to be sure it is ok to remove the neck and head from the dend list
    #     icell.dend.append(head)
    # else:
    #     icell.apical.append(head)
    sim.neuron.h.pop_section()
    for sec in [neck, head]:
        sec.insert("pas")
    neck.g_pas = 1.0 / passive_val["RM"]
    neck.cm= passive_val["CM"]
    neck.Ra=passive_val["RA"]#int(Rneck)
    # neck.e_pas=E_pas
    # head.e_pas=icell.soma[0].e_pas
    return [neck, head]


def add_morph(sim, icell, syns, spine_properties):#,spine_property=self.spine_propertie
    all = []
    # sim.neuron.h.execute('create spineNeck['+str(len(syns))+']', icell)
    # sim.neuron.h.execute('create spineHead['+str(len(syns))+']', icell)
    for i, syn in enumerate(syns):
        num = syn[0]
        num = int(num[num.find("[") + 1:num.find("]")])
        if syn[0].find("dend") > -1:
            sec = icell.dend[num]
        elif syn[0].find("apic") > -1 :
            sec = icell.apic[num]
        else:
            sec = list(icell.soma)[0]
        all.append(create_spine(sim, icell, sec, syn[1], i, neck_diam=spine_properties[i]['NECK_DIAM'], neck_length=spine_properties[i]['NECK_LENGHT'],
                            head_diam=spine_properties[i]['HEAD_DIAM']))
    return all
