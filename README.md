# Simulation
Simulation Project

The idea of this simulation is the identify patterns and try to analyse real world
behavior of people in a endemic, or pandemic, environment.

We will need, basically, an environment and agents. The environment is going to 
be a city, that contains severall regions. Regions will be separated in domestic,
industrial and commercial:
    
    Domestic Regions: will contain the homes of our agents, our population. The
    amount of houses and individuals living in a single house will vary randomly, and will be
    dependent on the distance of the centroid of the region, to the center of the city,
    that will be an input to be speciffied.Further from the city center means more houses
    will be contained in a region and more people will live in a single house. This is
    an attempt to emmulate the rich and poor regions of a real city, and it's distribution.
    Each region will be initialized with a distance from the city center, and a random radius size.

    Commercial Regions: this kind of region will be the place where agents commute to
    and spend the majority of their time and are the most exposed to be inffected.
    This type of region will contain Restaurants, Hospitals and Workplaces. Restaurants
    will contain a higher amount of agents and workplaces will contain a random number of workers.
    Hospital will contain workers and pacients and also a large amount of agents.

    Industrial Regions: this type of regions will contain fewer buildings but will
    have a larger concentration of workers that will spend more time together.

 ------------------------      #################      ------------------------
 
Our agents will be derived from the class Person:
    
    Person: will have an object Home that will always come back to, and share with
    other agents Person. Will have various traits that will dictate how it will behave, 
    for example: (social) resistance(the major interest feature of this project), fanciness (dictates the
    transportation type and lunch routine, affected by domestic region type), influence (dictates how it spreds its
    resistance to others, and how others affect its own resistance), age, chronic disease probability and intensity.

    
And each agents will have 5 possible states:
    
    Susceptible: will be susceptible to be contaminated if exposed. The susceptible agent
    will aslo have a trait called protection, which is determined by the person's resistance parameter.
    It affects the probabilty of being contaminated if exposed to an infected agent.
    
    Infected: when infected, an agent will first spend 2~5 days (randomly) before noticing symptoms.
    After this time, the symptoms of the agennt will be determined by the symptoms type probability (influenced by age 
    and chroninc disease), depending on the symptoms type and others, the agent will have a pacient probability,
    which is the probability of the agent occupying a place in the hospital. The behaviour of the infect agent
    will be dictated by the person's resistance parameter. The trait home_office is dependent of the workplace
    and grants the agent the possibility of isolating themselves, situation that will be affect by the agent's resistance factor.
    In case of symptoms type 3, the infected agent will be placed in the hospital, if there is space, if there is no space
    the death probability will greatly rise. There is also a contagius factor of the infected agent, dictated by it's resistance
    and symptoms, and home_office factor, it models how likely the infected agent is to infect other susceptible agents.
    The infected agent will spend 10~18 days as infected, if it doesn't evolves into a Pacient agent,  at the end
    of this time, the agent will turn into an Immune agent.
    
        Pacient: If the infected agent develops symptoms type 3, they will be placed in a Hospital as a Pacient agent.
    The agent will have a death probability curve, that depends on age and chronic disease, and evolves through time.
    Each agent will spend a certain recovery time in the hospital, 10~20 days. At the end of this period, the agent, if it 
    survives, will go back home and turn into an Immune agent. Otherwise, the agent will die, and be remove from the population.
    Pacient agents that survives this stage will have its disease factor increased by a random amount, that will lasts for some months
    representing the sequelea of the infeciton.

    Immune: Immune agents will return to is regular routine, and will stay protected against the infection
    for a time, 4~8 months. After that, they return to being a Susceptible agent again.
        
    Dead: the Pacients agents that didn't survived the infection.
