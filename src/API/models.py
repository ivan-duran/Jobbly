from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, Real
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30))
    second_name = Column(String(30))
    lastname = Column(String(30))
    mail = Column(String(30), unique=True, nullable=False)
    phone_number = Column(Integer, unique=True, nullable=False)
    address = Column(String(30))
    digit_number_rut = Column(String(1), nullable=False)
    rut_numbers = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    calification = Column(Real, nullable=False)

    # Define relaciones
    logins = relationship("UserLogin", back_populates="user")
    worker = relationship("Worker", back_populates="user", uselist=False)
    petitioner = relationship("Petitioner", back_populates="user", uselist=False)


class UserLogin(Base):
    __tablename__ = "user_login"

    id = Column(Integer, primary_key=True, index=True)
    main = Column(String(30), unique=True, nullable=False)
    pass_hash = Column(String(128), unique=True, nullable=False)  # Recomendación: almacenar contraseñas cifradas
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="logins")


class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Definir relaciones
    user = relationship("User", back_populates="worker")
    services = relationship("Service", back_populates="worker")


class Petitioner(Base):
    __tablename__ = "petitioner"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Definir relaciones
    user = relationship("User", back_populates="petitioner")
    requests = relationship("Request", back_populates="petitioner")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    id_worker = Column(Integer, ForeignKey("worker.id", ondelete="CASCADE"))
    content = Column(Text)
    init_date = Column(Date, nullable=False)
    finish_date = Column(Date)
    price = Column(Integer, nullable=False)

    # Definir relaciones
    worker = relationship("Worker", back_populates="services")
    petitioner_services = relationship("PetitionerService", back_populates="service")


class PetitionerService(Base):
    __tablename__ = "petitioner_services"

    id = Column(Integer, primary_key=True, index=True)
    id_services = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    id_petitioner = Column(Integer, ForeignKey("petitioner.id", ondelete="CASCADE"))
    petition_date = Column(Date, nullable=False)
    solved = Column(Boolean)

    # Definir relaciones
    service = relationship("Service", back_populates="petitioner_services")
    petitioner = relationship("Petitioner", back_populates="petitioner_services")
    evaluation_petitioner = relationship("EvaluationPetitioner", back_populates="petitioner_service", uselist=False)
    evaluation_worker = relationship("EvaluationWorker", back_populates="petitioner_service", uselist=False)


class EvaluationPetitioner(Base):
    __tablename__ = "evaluation_petitioner"

    id = Column(Integer, primary_key=True, index=True)
    id_petitioner_services = Column(Integer, ForeignKey("petitioner_services.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    petitioner_service = relationship("PetitionerService", back_populates="evaluation_petitioner")

class EvaluationWorker(Base):
    __tablename__ = "evaluation_worker"

    id = Column(Integer, primary_key=True, index=True)
    id_petitioner_services = Column(Integer, ForeignKey("petitioner_services.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    petitioner_service = relationship("PetitionerService", back_populates="evaluation_worker")


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    id_petitioner = Column(Integer, ForeignKey("petitioner.id", ondelete="CASCADE"))
    init_date = Column(Date, nullable=False)
    finish_date = Column(Date)
    price = Column(Integer, nullable=False)

    # Definir relaciones
    petitioner = relationship("Petitioner", back_populates="requests")
    worker_requests = relationship("WorkerRequest", back_populates="request")


class WorkerRequest(Base):
    __tablename__ = "worker_request"

    id = Column(Integer, primary_key=True, index=True)
    id_worker = Column(Integer, ForeignKey("worker.id", ondelete="CASCADE"))
    id_request = Column(Integer, ForeignKey("request.id", ondelete="CASCADE"))
    petition_date = Column(Date, nullable=False)
    solved = Column(Boolean)

    # Definir relaciones
    worker = relationship("Worker", back_populates="worker_requests")
    request = relationship("Request", back_populates="worker_requests")
    petitioner_review = relationship("PetitionerReview", back_populates="worker_request", uselist=False)
    worker_review = relationship("WorkerReview", back_populates="worker_request", uselist=False)


class PetitionerReview(Base):
    __tablename__ = "petitioner_review"

    id = Column(Integer, primary_key=True, index=True)
    id_worker_request = Column(Integer, ForeignKey("worker_request.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    worker_request = relationship("WorkerRequest", back_populates="petitioner_review")


class WorkerReview(Base):
    __tablename__ = "worker_review"

    id = Column(Integer, primary_key=True, index=True)
    id_worker_request = Column(Integer, ForeignKey("worker_request.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    worker_request = relationship("WorkerRequest", back_populates="worker_review")