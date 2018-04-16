from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setupDatabase import Base, Catalog, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/\
             18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Item for Fridrich Nietzsche
catalog1 = Catalog(
   user_id=1, catalogname="Fridrich Nietzsche", description="Friedrich Nietzsche \
   (1844–1900) was a German philosopher and \
   cultural critic who published intensively in the 1870s and 1880s. He is \
   famous for uncompromising criticisms of traditional European morality and \
   religion, as well as of conventional philosophical ideas and social and \
   political pieties associated with modernity. Many of these criticisms \
   rely on psychological diagnoses that expose false consciousness infecting \
   people’s received ideas; for that reason, he is often associated with a \
   group of late modern thinkers (including Marx and Freud) who advanced a \
   “hermeneutics of suspicion” against traditional values (see Foucault \
   [1964] 1990, Ricoeur [1965] 1970, Leiter 2004). Nietzsche also used his \
   psychological analyses to support original theories about the nature of \
   the self and provocative proposals suggesting new values that he thought \
   would promote cultural renewal and improve social and psychological life \
   by comparison to life under the traditional values he criticized."
)

session.add(catalog1)
session.commit()

Item1 = Item(
   user_id=1, itemname="Thus Spoke Zarathustra", description="One of the most  \
   famous philosophical book of the last 150 \
   years was published in 1892. Even the most unfamiliar with philosophy \
   have it in their library, or have at least heard about Thus Spoke \
   Zarathustra. Nietzsche described it as his deepest philosophical work, \
   the most representative reflection of his thinking and vision, referring \
   to the issue of the death of God and Übermensch‘s appearance.",
   year="1892", catalog=catalog1
)

session.add(Item1)
session.commit()


Item2 = Item(
   user_id=1, itemname="On the Genealogy of Morality",
   description="Arguably the most systematic and coherent of \
   Nietzsche’s works, On the Genealogy of Morality deals with – and, \
   actually, confronts – the value system of the West, as a system that \
   captures man’s freedom, weakens his existence and undermines knowledge \
   through religion, ethics and philosophy. The German philosopher suggests \
   the rejection of this ‘slave morality’ and supports the Übermensch, \
   who will overcome all these obstacles to reach freedom and knowledge.",
   year="1887", catalog=catalog1
)

session.add(Item2)
session.commit()

Item3 = Item(
   user_id=1, itemname="The Antichrist",
   description="“Christianity remains to this day the greatest misfortune \
   of humanity.” This sentence sums up the basic idea and the sarcastic \
   tone of The Antichrist, so if you’re pissed off by reading just that, \
   don’t go for the rest. Even though Nietzsche had a religious upbringing, \
   this book is a criticism of the new ideas of Christianity that, \
   according to the philosopher, destroyed the ancient world, the only \
   real civilization. He does not put the blame on Christ, he stands \
   for him, but does not hesitate to criticize his representatives and \
   the destructive religious status quo.",
   year="1888", catalog=catalog1
)

session.add(Item3)
session.commit()

Item4 = Item(
   user_id=1, itemname="The Birth of Tragedy",
   description="The first work Nietzsche published describes the tragic \
   feeling of life, as a typical philosophical aspect of modernity. \
   According to the German existentialist, this feeling is mainly expressed \
   through music, therefore tragedy played a dominant role within the \
   framework of the aesthetic conceptions through the consecutive eras.",
   year="1872", catalog=catalog1
)

session.add(Item4)
session.commit()

Item5 = Item(
   user_id=1, itemname="Ecce Homo",
   description="Nietzsche autobiography was composed just weeks before \
   the writer collapsed into madness. Here were are given an examination \
   of the philosopher himself, as Nietzsche traces his life, work examines \
   his influences and his eventually toppling \
   of them with stunning revelations.",
   year="1883", catalog=catalog1
)

session.add(Item5)
session.commit()


# Item for Søren Kierkegaard
catalog2 = Catalog(
   user_id=1, catalogname="Søren Kierkegaard",
   description="Søren Aabye Kierkegaard (b. 1813, d. 1855) was a profound \
   and prolific writer in the Danish “golden age” of intellectual and \
   artistic activity. His work crosses the boundaries of philosophy, \
   theology, psychology, literary criticism, devotional literature \
   and fiction. Kierkegaard brought this potent mixture of discourses to \
   bear as social critique and for the purpose of renewing Christian faith \
   within Christendom. At the same time he made many original conceptual \
   contributions to each of the disciplines he employed. He is known as the \
   “father of existentialism”, but at least as important are his critiques \
   of Hegel and of the German romantics, his contributions to the \
   development of modernism, his stylistic experimentation, his vivid \
   re-presentation of biblical figures to bring out their modern relevance, \
   his invention of key concepts which have been explored and redeployed by \
   thinkers ever since, his interventions in contemporary Danish church \
   politics, and his fervent attempts to analyse and \
   revitalise Christian faith."
)

session.add(catalog2)
session.commit()


Item1 = Item(
   user_id=1, itemname="Fear and Trembling",
   description="In Fear and Trembling, Kierkegaard wanted to understand \
   the anxiety that must have been present in Abraham when God commanded him \
   to offer his son as a human sacrifice. Abraham had a choice to complete \
   the task or to forget it. He resigned himself to the loss of his son, \
   acting according to his faith. In other words, one must be willing to \
   give up all his or her earthly possessions in infinite resignation and \
   must also be willing to give up whatever it is that he or she loves \
   more than God. Abraham had passed the test -- his love for God proved \
   greater than anything else in him. And because a good and just Creator \
   would not want a father to kill his son, God intervened at the last \
   moment to prevent the sacrifice.",
   year="1843", catalog=catalog2
)

session.add(Item1)
session.commit()

Item2 = Item(
   user_id=1, itemname="The Sickness Unto Death",
   description=" A famous duck dish from Beijing that \
   has been prepared since the imperial era. The meat \
   is prized for its thin, crisp skin, with authentic \
   versions of the dish serving mostly the skin and \
   little meat, sliced in front of the diners by the cook",
   year="1849", catalog=catalog2
)

session.add(Item2)
session.commit()


# Item for Fyodor Dostoyevsky
catalog3 = Catalog(
   user_id=1, catalogname="Fyodor Dostoyevsky",
   description='Fyodor Dostoyevsky, in full Fyodor Mikhaylovich Dostoyevsky, \
   Dostoyevsky also spelled Dostoevsky, (born November 11 \
   [October 30, Old Style], 1821, Moscow, Russia—died February 9 \
   [January 28, Old Style], 1881, St. Petersburg), Russian novelist and \
   short-story writer whose psychological penetration into the darkest \
   recesses of the human heart, together with his unsurpassed moments of \
   illumination, had an immense influence on 20th-century fiction. \
   Dostoyevsky is usually regarded as one of the finest novelists who ever \
   lived. Literary modernism, existentialism, and various schools of \
   psychology, theology, and literary criticism have been profoundly shaped \
   by his ideas. His works are often called prophetic because he so \
   accurately predicted how Russia’s revolutionaries would behave if they \
   came to power. In his time he was also renowned for \
   his activity as a journalist.'
)

session.add(catalog3)
session.commit()


Item1 = Item(
   user_id=1, itemname="The Brothers Karamazov ",
   description="The Brothers Karamazov is one of the passionate and best \
   fyodor dostoevsky books in order philosophical novel set in the 19th \
   century Russia. During the time, Russia was deeply in the ethical \
   debates of God, morality and free will. The Brothers Karamazov is \
   the spiritual drama of moral struggles that are mainly concerned with \
   the faith, reason, and doubt that sets against the modernizing Russia. \
   When brutal landowner Fyodor Karamazov was murdered, lives of his sons \
   become so much changed into the irrevocably",
   year="1880", catalog=catalog3
)

session.add(Item1)
session.commit()

Item2 = Item(
   user_id=1, itemname="Crime and Punishment",
   description="Raskolnikov is a talented student and poverty strikes him \
   with devising the theory about the extraordinary men who are seen above \
   the law. With brilliance and innovation, he makes the new suggestion that \
   contributes the society. Raskolnikov sets out to prove the theory with \
   murdering the cynical, vile and old pawnbroker with her sister.",
   year="1866", catalog=catalog3
)

session.add(Item2)
session.commit()

Item3 = Item(
   user_id=1, itemname="The Idiot",
   description="After returning to Russia from the sanitarium in \
   Switzerland, Christ-like epileptic Prince Myshkin also finds himself \
   most enmeshed in the tangle of love that has torn the two women. Nastasya \
   and Aglaia is the notorious woman both involved with the money hungry and \
   corrupt Ganya. Honesty, goodness, and integrity of Myshkin shown with the \
   unequal attributes bring more emptiness around him. Anna Brailovsky \
   corrected inaccuracies that are wrought by the drastic anglicization of \
   the novel by Garnett.",
   year="1869", catalog=catalog3
)

session.add(Item3)
session.commit()

Item4 = Item(
   user_id=1, itemname="Notes from Underground", description="This is a \
   collection of powerful stories by great masters of Russian literature, \
   Fyodor Dostoyevsky. The author illustrates thoughts on political \
   philosophy, humanity, and religion. Notes from Underground, White Nights, \
   The Dream of a Ridiculous Man, and Selections from The House of the Dead \
   compels the works presented with greater volume that is written at the \
   distinct periods of Dostoyevsky's life. Thomas Mann has described the \
   famous Dostoyevsky as the author whose Christian sympathy is quite \
   ordinarily devoted to solving the problems based on human misery, sin, \
   depths of lust as well as crime.",
   year="1864", catalog=catalog3
)

session.add(Item4)
session.commit()


Item5 = Item(
   user_id=1, itemname="Demons",
   description='Demons by Fyodor Dostoevsky were inspired by the true story \
   of political murder in Russians in 1869. Fyodor Dostoevsky has conceived \
   of the demons as the "novel-pamphlet" and everything has been plagued \
   with the ideology of materialists. Fyodor Dostoevsky saw something that \
   infects the native land and emerged as the most prophetic as well as \
   ferociously funny masterpiece. Pyotr and Stavrogin were considered as \
   the leaders of Russian revolutionary cell.',
   year="1872", catalog=catalog3
)

session.add(Item5)
session.commit()

Item6 = Item(
   user_id=1, itemname="The House of the Dead",
   description="The House of the Dead is the fiction story that is based \
   on 4 years of life in a Siberian prison. An educated upper-class man was \
   condemned to live with the brutal guards and criminals with the arbitrary \
   punishments, disgusting living conditions, lousy food and much more. \
   He avoids recrimination and bitterness along with the faith in \
   the human survival.",
   year="1862", catalog=catalog3
)

session.add(Item6)
session.commit()

# Item for Jean-Paul Sartre
catalog4 = Catalog(
   user_id=1, catalogname="Jean-Paul Sartre",
   description='''Sartre (1905–1980) is arguably the best known philosopher \
   of the twentieth century. His indefatigable pursuit of philosophical \
   reflection, literary creativity and, in the second half of his life, \
   active political commitment gained him worldwide renown, if not \
   admiration. He is commonly considered the father of Existentialist \
   philosophy, whose writings set the tone for intellectual life in the \
   decade immediately following the Second World War. Among the many \
   ironies that permeate his life, not the least is the immense popularity \
   of his scandalous public lecture “Existentialism is a Humanism,” \
   delivered to an enthusiastic Parisian crowd October 28, 1945. Though \
   taken as a quasi manifesto for the Existentialist movement, the \
   transcript of this lecture was the only publication that Sartre openly \
   regretted seeing in print. And yet it continues to be the major \
   introduction to his philosophy for the general public. One of the reasons \
   both for its popularity and for his discomfort is the clarity with which \
   it exhibits the major tenets of existentialist thought while revealing \
   Sartre's attempt to broaden its social application in response to his \
   Communist and Catholic critics. In other words, it offers us a glimpse of \
   Sartre's thought “on the wing.” After surveying the evolution of Sartre's \
   philosophical thinking, I shall address his thought under five categories, \
   namely, ontology, psychology, ethics, political commitment, and the \
   relation between philosophy and the fine arts, especially literature, \
   in his work. I shall conclude with several observations about the \
   continued relevance of his thought in contemporary philosophy both \
   Anglo-American and “Continental.”'''
)

session.add(catalog4)
session.commit()


Item1 = Item(
   user_id=1, itemname="Being and Nothingness",
   description='A philosophical classic and major cornerstone of modern \
   existentialism. Often criticized and all-too-rarely understood, \
   the philosophy of Jean-Paul Sartre encompasses the dilemmas and \
   aspirations of the individual in contemporary society.Being and \
   Nothingnesscontains all the basic tenets of his thought, as well as \
   all its more intricate details. A work of inherent force and epic scope, \
   it provides a vivid analysis for all who would understand one of the most \
   influential philosophic movements of any age, and makes clear whyThe New \
   York Timeshailed Sartre’s masterpiece as "a philosophy to be reckoned \
   with, both for its own intrinsic power and as a profound symptom of \
   our time."',
   year="1943", catalog=catalog4
)

session.add(Item1)
session.commit()

Item2 = Item(
   user_id=1, itemname="Nausea",
   description='''Nausea is the story of Antoine Roquentin, a French writer \
   who is horrified at his own existence. In impressionistic, diary form he \
   ruthlessly catalogues his every feeling and sensation about the world and \
   people around him. His thoughts culminate in a pervasive, overpowering \
   feeling of nausea which "spread at the bottom of the viscous puddle, at \
   the bottom of our time, the time of purple suspenders and broken chair \
   seats; it is made of wide, soft instants, spreading at the edge, like an \
   oil stain." Roquentin's efforts to come to terms with his life, his \
   philosophical and psychological struggles, give Sartre the opportunity to \
   dramatize the tenets of his Existentialist creed. The introduction for \
   this edition of Nausea by Hayden Carruth gives background on Sartre's life \
   and major works, a summary of the principal themes of Existentialist \
   philosophy, and a critical analysis of the novel itself.''',
   year="1938", catalog=catalog4
)

session.add(Item2)
session.commit()


# Item for Immanuel Kant
catalog5 = Catalog(
   user_id=1, catalogname="Immanuel Kant",
   description='''Immanuel Kant (1724–1804) is the central figure in modern \
   philosophy. He synthesized early modern rationalism and empiricism, \
   set the terms for much of nineteenth and twentieth century philosophy, \
   and continues to exercise a significant influence today in metaphysics, \
   epistemology, ethics, political philosophy, aesthetics, and other fields. \
   The fundamental idea of Kant's “critical philosophy” — especially in his \
   three Critiques: the Critique of Pure Reason (1781, 1787), the Critique \
   of Practical Reason (1788), and the Critique of the Power of Judgment \
   (1790) — is human autonomy. He argues that the human understanding is the \
   source of the general laws of nature that structure all our experience; \
   and that human reason gives itself the moral law, which is our basis for \
   belief in God, freedom, and immortality. Therefore, scientific knowledge, \
   morality, and religious belief are mutually consistent and secure because \
   they all rest on the same foundation of human autonomy, which is also the \
   final end of nature according to the teleological worldview of reflecting \
   judgment that Kant introduces to unify the theoretical and practical \
   parts of his philosophical system.'''
)

session.add(catalog5)
session.commit()


Item1 = Item(
   user_id=1, itemname="Critique of Pure Reason",
   description="The Critique of Pure Reason, published by Immanuel Kant in \
   1781, is one of the most complex structures and the most significant of \
   modern philosophy, bringing a revolution at least as great as that of \
   Descartes and his Discourse on Method. The complexity of the first \
   review (the second is the critique of practical reason, and the third \
   is a critique of the faculty of judging), is such that Kant himself \
   published an introductory text, entitled Prolegomena to Any Future \
   Metaphysics. The aim of this book is summed up quite easily, however: \
   metaphysics is a battle that needs to be ordered. Kant proposes to \
   everyone agreed, giving a new status to reason and new contours to \
   the understanding. In summary, the critique of pure reason tries to \
   define credible to the question: How do I know? To this question Kant \
   answers, I can think of the objects of metaphysics (God, I, the world), \
   but not knowing in the sense that I know the laws of physics.",
   year="1781", catalog=catalog5
)

session.add(Item1)
session.commit()

Item2 = Item(
   user_id=1, itemname="Critique of Practical Reason",
   description="Critique of Practical Reason, written by legendary author \
   Immanuel Kant is widely considered to be one of the greatest classic and \
   historical texts of all time. This great classic will surely attract a \
   whole new generation of readers. For many, Critique of Practical Reason \
   is required reading for various courses and curriculums. And for others \
   who simply enjoy reading timeless pieces of classic literature, this gem \
   by Immanuel Kant is highly recommended. Published by Classic Books \
   International and beautifully produced, Critique of Practical Reason \
   would make an ideal gift and it should be a part of everyone's \
   personal library.",
   year="1788", catalog=catalog5
)

session.add(Item2)
session.commit()

Item3 = Item(
   user_id=1, itemname="Critique of Judgment",
   description="In THE CRITIQUE OF JUDGMENT (1790), Immanuel Kant \
   (1724-1804) seeks to establish the a priori principles underlying the \
   faculty of judgment, just as he did in his previous critiques of pure \
   and practical reason. The first part deals with the subject of our \
   aesthetic sensibility; we respond to certain natural phenomena as \
   beautiful, says Kant, when we recognize in nature a harmonious order \
   that satisfies the mind's own need for order. The second half of the \
   critique concentrates on the apparent teleology in nature's design of \
   organisms. Kant argues that our minds are inclined to see purpose and \
   order in nature and this is the main principle underlying all of our \
   judgments. Although this might imply a super sensible Designer, Kant \
   insists that we cannot prove a supernatural dimension or the existence \
   of God. Such considerations are beyond reason and are solely the \
   province of faith.",
   year="1790", catalog=catalog5
)

session.add(Item3)
session.commit()


# Item for Plato
catalog6 = Catalog(
   user_id=1, catalogname="Plato",
   description='Plato (429?–347 B.C.E.) is, by any reckoning, one of the \
   most dazzling writers in the Western literary tradition and one of the \
   most penetrating, wide-ranging, and influential authors in the history of \
   philosophy. An Athenian citizen of high status, he displays in his works \
   his absorption in the political events and intellectual movements of \
   his time, but the questions he raises are so profound and the strategies \
   he uses for tackling them so richly suggestive and provocative that \
   educated readers of nearly every period have in some way been influenced \
   by him, and in practically every age there have been philosophers \
   who count themselves Platonists in some important respects. He was not \
   the first thinker or writer to whom the word “philosopher” should be \
   applied. But he was so self-conscious about how philosophy should be \
   conceived, and what its scope and ambitions properly are, and he so \
   transformed the intellectual currents with which he grappled, that the \
   subject of philosophy, as it is often conceived—a rigorous and systematic \
   examination of ethical, political, metaphysical, and epistemological \
   issues, armed with a distinctive method—can be called his invention. \
   Few other authors in the history of Western philosophy approximate him \
   in depth and range: perhaps only Aristotle (who studied with him), \
   Aquinas, and Kant would be generally agreed to be of the same rank.'
)

session.add(catalog6)
session.commit()


Item1 = Item(
   user_id=1, itemname="Apology",
   description="The Apology is one of those rare works that gracefully \
   bridges the divide between philosophy and literature. The work is less \
   concerned with asserting any particular philosophical doctrines than it \
   is with creating a portrait of the ideal philosopher. On trial, with his \
   life at stake, Socrates maintains his cool and unwaveringly defends his \
   way of life as unassailably just. This speech has served as inspiration \
   and justification for philosophical thinkers ever since. It is also \
   valuable in that it links three major themes in Socratic thought: \
   Socratic irony, the elenchus (the Socratic mode of inquiry), and the \
   higher ethical concerns that dominate Socrates' life. The Delphic oracle, \
   which proclaimed that Socrates was the wisest of men because he knows \
   that he knows nothing, can be posited as the source of Socratic irony. \
   This oracle has led Socrates to assume his highly ironic stance of \
   confessing his own ignorance, and yet showing his interlocutors to be \
   even more ignorant than he; great wisdom turns out, contrary to \
   expectation, to reside in a humble acknowledgment of ignorance. With \
   wisdom of this kind, Socrates does not take himself too seriously. \
   Indeed, his wisdom is deeply humbling, as it casts all pretensions to \
   human knowledge into question. With a smile, Socrates accepts that he \
   is better off the less he thinks he knows, and passes this wisdom along \
   with appropriate wit. This irony, then, deeply informs the elenchus, \
   Socrates' preferred mode of inquiry. It is important to note that almost \
   all written accounts of Socrates are dialogues (The Apology is an \
   exception)--Socrates never lectures on his beliefs in a one-sided manner. \
   This supports the idea that Socrates has no knowledge of his own to put \
   forward. His method of inquiry consists of identifying what his \
   interlocutor thinks he knows, and then slowly dissecting those claims \
   of knowledge. The Apology, however, is presented almost exclusively in \
   the form of a monologue, because Socrates is not discussing and \
   dismantling any one particular claim so much as he is laying out the \
   method behind these dismantlings. As such, it is an invaluable \
   commentary on the other dialogues. The elenchus acts to disabuse \
   Socrates' interlocutors of their pretensions and thereby deepens their \
   wisdom. For Socrates, wisdom and virtue are closely connected, so his \
   efforts serve to improve society as a whole. In Socrates' view, if we are \
   all wise, none of us will ever do wrong, and our self-knowledge will lead \
   to healthier, more fulfilling lives. Thus, the philosopher, according to \
   Socrates, does not merely follow abstract intellectual pursuits for the \
   sake of amusement, but is engaged in activities \
   of the highest moral value.",
   year="399BC", catalog=catalog6
)

session.add(Item1)
session.commit()

Item2 = Item(
   user_id=1, itemname="Republic",
   description="Since the mid-nineteenth century, the Republic has been \
   Plato’s most famous and widely read dialogue.  As in most other Platonic \
   dialogues the main character is Socrates.  It is generally accepted that \
   the Republic belongs to the dialogues of Plato’s middle period. \
   In Plato’s early dialogues, Socrates refutes the accounts of his \
   interlocutors and the discussion ends with no satisfactory answer to the \
   matter investigated.  In the Republic however, we encounter Socrates \
   developing a position on justice and its relation to eudaimonia \
   (happiness). He provides a long and complicated, but unified argument, in \
   defense of the just life and its necessary connection to the happy life. \
   The dialogue explores two central questions.  The first question is “what \
   is justice?”  Socrates addresses this question both in terms of political \
   communities and in terms of the individual person or soul.  He does this \
   to address the second and driving question of the dialogue: “is the just \
   person happier than the unjust person?” or “what is the relation of \
   justice to happiness?” Given the two central questions of the discussion, \
   Plato’s philosophical concerns in the dialogue are ethical and political. \
   In order to address these two questions, Socrates and his interlocutors \
   construct a just city in speech, the Kallipolis.  They do this in order \
   to explain what justice is and then they proceed to illustrate justice by \
   analogy in the human soul.  On the way to defending the just life, \
   Socrates considers a tremendous variety of subjects such as several rival \
   theories of justice, competing views of human happiness, education, the \
   nature and importance of philosophy and philosophers, knowledge, \
   the structure of reality, the Forms, the virtues and vices, good and \
   bad souls, good and bad political regimes, the family, the role of women \
   in society, the role of art in society, and even the afterlife.  \
   This wide scope of the dialogue presents various interpretative \
   difficulties and has resulted in thousands of scholarly works.  \
   In order to attempt to understand the dialogue’s argument as a \
   whole one is required to grapple with these subjects.",
   year="381BC", catalog=catalog6
)

session.add(Item2)
session.commit()


print("added menu items!")
