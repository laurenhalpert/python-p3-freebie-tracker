from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Freebie(Base):
    __tablename__ = 'freebies'
    def __init__(self, company_id, dev_id, item_name, value, id = None):
        self.id = id
        self.company_id = Column(Integer(), ForeignKey('companies.id'))
        self.dev_id = Column(Integer(), ForeignKey('devs.id'))
        self.item_name = item_name
        self.value = value

    id=Column(Integer(), primary_key=True)
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    item_name=Column(String())
    value=Column(Integer())

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'

    def __repr__(self):
        return f'<Freebie {self.item_name}>'

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', backref='company')
    devs = association_proxy('freebies', 'dev',
        creator=lambda dv: Freebie(dev=dv))
    def give_freebie(self, dev, item_name, value):
        #creates a new freebie instance associated with THIS company and the given dev
        return Freebie(self.id, dev.id, item_name, value)
    @classmethod
    def oldest_company(cls):
        oldest= session.query(cls).order_by(cls.founding_year).first()
        return oldest
    def __repr__(self):
        return f'<Company {self.name}>'




class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', backref='dev')
    companies = association_proxy('freebies', 'company',
        creator=lambda cm: Freebie(company=cm))

    def received_one(self, item_name):
        #if any freebies' item names are the item_name return True, else False
        for freebie in self.freebies:
            return freebie.item_name == item_name

    def give_away(self, dev, freebie):
        #updates given freebie's dev to be the given dev iff freebie's current dev is the one that the method is being called on
        if freebie.dev_id == self.id:
            freebie.dev_id = dev.id
        return freebie.dev_id
    def __repr__(self):
        return f'<Dev {self.name}>'


