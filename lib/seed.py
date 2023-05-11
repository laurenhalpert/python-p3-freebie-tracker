#!/usr/bin/env python3

from random import choice as rc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from models import Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()



def delete_records():
    session.query(Company).delete()
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.commit()

def create_records():
    companies = [
        Company(
            name= 'Bob',
            founding_year = random.randint(1900, 2023)
        ) for i in range(100)]
    freebies = [
        Freebie(
            company_id = random.randint(1,100),
            dev_id = random.randint(1, 500),
            item_name='item',
            value=random.randint(0, 60),
        ) for i in range(1000)]
    devs = [
        Dev(
            name= "Devonne"
        ) for i in range(500)]
    session.add_all(companies + freebies + devs)
    session.commit()
    return companies, freebies, devs

def relate_records(companies, freebies, devs):
    for freebie in freebies:
        freebie.dev = rc(devs)
        freebie.company = rc(companies)

    session.add_all(freebies)
    session.commit()

if __name__ == '__main__':
    delete_records()
    companies, freebies, devs = create_records()
    relate_records(companies, freebies, devs)