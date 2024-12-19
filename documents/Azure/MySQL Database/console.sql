create database delawarexhowest;
use delawarexhowest;

DROP TABLE IF EXISTS project_assignments;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projectTitle VARCHAR(255) NOT NULL,
    dateStarted DATETIME NOT NULL,
    isActive BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(100) NOT NULL,
    isAvailable BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE project_assignments (
     id INT AUTO_INCREMENT PRIMARY KEY,
     projectId INT NOT NULL,
     employeeId INT NOT NULL,
     assignedDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (projectId) REFERENCES projects(id) ON DELETE CASCADE,
     FOREIGN KEY (employeeId) REFERENCES employees(id) ON DELETE CASCADE
);


CREATE TABLE roles_rates (
                             id INT AUTO_INCREMENT PRIMARY KEY,
                             role VARCHAR(100) NOT NULL,
                             rate DECIMAL(10, 2) NOT NULL
);




INSERT INTO projects (projectTitle, dateStarted, isActive) VALUES
    ('Website Redesign', '2023-01-10', TRUE),
    ('Mobile App Development', '2023-03-05', TRUE),
    ('Data Analysis Project', '2023-04-20', FALSE),
    ('Marketing Campaign', '2023-05-15', TRUE),
    ('Internal Training Program', '2023-06-01', FALSE);


# Possible roles:
    # "0 Blended FE dev",
    # "0 Blended MW dev",
    # "0 Blended Overall dev,
    # "0 Blended XR dev",
    # "1 Analyst",
    # "2 Consultant Technical",
    # "3 Senior Consultant Technical",
    # "4 Lead Expert",
    # "5 Manager",
    # "6 Senior Manager",
    # "7 DPH Consultant Technical",
    # "8 DPH Senior Consultant Technical",
    # "9 DPH Lead Expert/Manager"



INSERT INTO employees (firstname, lastname, email, role, isAvailable) VALUES
                                                                          -- 0 Blended FE dev
                                                                          ('Patrizia', 'Verboom', 'patrizia.verboom@delaware.com', '0 Blended FE dev', TRUE),
                                                                          ('Mirthe', 'Hawkins', 'mirthe.hawkins@delaware.com', '0 Blended FE dev', TRUE),
                                                                          ('Douglas', 'Matias', 'douglas.matias@delaware.com', '0 Blended FE dev', FALSE),
                                                                          ('Lizzy', 'Ughi', 'lizzy.ughi@delaware.com', '0 Blended FE dev', FALSE),
                                                                          ('Zoe', 'Tavares', 'zoe.tavares@delaware.com', '0 Blended FE dev', FALSE),
                                                                          ('Wenzel', 'Begue', 'wenzel.begue@delaware.com', '0 Blended FE dev', TRUE),
                                                                          ('Erica', 'Hampton', 'erica.hampton@delaware.com', '0 Blended FE dev', TRUE),
                                                                          ('Julie', 'van der Klijn', 'julie.van der klijn@delaware.com', '0 Blended FE dev', TRUE),
                                                                          ('Gunnar', 'Rizzo', 'gunnar.rizzo@delaware.com', '0 Blended FE dev', FALSE),
                                                                          ('Baptist', 'Michiels', 'baptist.michiels@delaware.com', '0 Blended FE dev', TRUE),
                                                                          -- 0 Blended MW dev
                                                                          ('America', 'Petersson', 'america.petersson@delaware.com', '0 Blended MW dev', TRUE),
                                                                          ('Alejandra', 'Hermann', 'alejandra.hermann@delaware.com', '0 Blended MW dev', FALSE),
                                                                          ('Sigvard', 'Vismara', 'sigvard.vismara@delaware.com', '0 Blended MW dev', TRUE),
                                                                          ('Nathan', 'Heymans', 'nathan.heymans@delaware.com', '0 Blended MW dev', FALSE),
                                                                          ('Alain', 'Josefsson', 'alain.josefsson@delaware.com', '0 Blended MW dev', TRUE),
                                                                          ('Valerie', 'Guarato', 'valerie.guarato@delaware.com', '0 Blended MW dev', TRUE),
                                                                          ('Sonia', 'Martin', 'sonia.martin@delaware.com', '0 Blended MW dev', TRUE),
                                                                          ('Fenna', 'Foucher', 'fenna.foucher@delaware.com', '0 Blended MW dev', TRUE),
                                                                          ('Ludvig', 'Nilsson', 'ludvig.nilsson@delaware.com', '0 Blended MW dev', FALSE),
                                                                          ('Dolores', 'Ferreira', 'dolores.ferreira@delaware.com', '0 Blended MW dev', FALSE),
                                                                          -- 0 Blended Overall dev
                                                                          ('Maria', 'Johansson', 'maria.johansson@delaware.com', '0 Blended Overall dev', FALSE),
                                                                          ('Hans', 'Jonsson', 'hans.jonsson@delaware.com', '0 Blended Overall dev', FALSE),
                                                                          ('Bo', 'Casini', 'bo.casini@delaware.com', '0 Blended Overall dev', TRUE),
                                                                          ('Eva', 'Persson', 'eva.persson@delaware.com', '0 Blended Overall dev', TRUE),
                                                                          ('Krista', 'Fiebig', 'krista.fiebig@delaware.com', '0 Blended Overall dev', TRUE),
                                                                          ('Nina', 'Weitzel', 'nina.weitzel@delaware.com', '0 Blended Overall dev', TRUE),
                                                                          ('Sven', 'Esteves', 'sven.esteves@delaware.com', '0 Blended Overall dev', TRUE),
                                                                          ('Calista', 'Mochlichen', 'calista.mochlichen@delaware.com', '0 Blended Overall dev', FALSE),
                                                                          ('Linnea', 'Nygren', 'linnea.nygren@delaware.com', '0 Blended Overall dev', TRUE),
                                                                          ('Agnes', 'Andre', 'agnes.andre@delaware.com', '0 Blended Overall dev', TRUE),
                                                                          -- 0 Blended XR dev
                                                                          ('Mirko', 'James', 'mirko.james@delaware.com', '0 Blended XR dev', TRUE),
                                                                          ('Robert', 'Marty', 'robert.marty@delaware.com', '0 Blended XR dev', FALSE),
                                                                          ('Jennifer', 'Romijn', 'jennifer.romijn@delaware.com', '0 Blended XR dev', FALSE),
                                                                          ('Nidia', 'Loiseau', 'nidia.loiseau@delaware.com', '0 Blended XR dev', FALSE),
                                                                          ('Karlijn', 'Svensson', 'karlijn.svensson@delaware.com', '0 Blended XR dev', FALSE),
                                                                          ('Brian', 'Bender', 'brian.bender@delaware.com', '0 Blended XR dev', TRUE),
                                                                          ('Josette', 'Respighi', 'josette.respighi@delaware.com', '0 Blended XR dev', FALSE),
                                                                          ('Lilia', 'Machado', 'lilia.machado@delaware.com', '0 Blended XR dev', TRUE),
                                                                          ('Dalila', 'Blin', 'dalila.blin@delaware.com', '0 Blended XR dev', TRUE),
                                                                          ('Osvaldo', 'Jesus', 'osvaldo.jesus@delaware.com', '0 Blended XR dev', TRUE),
                                                                          -- 1 Analyst
                                                                          ('Christelle', 'Olivetti', 'christelle.olivetti@delaware.com', '1 Analyst', FALSE),
                                                                          ('Elisabet', 'Campos', 'elisabet.campos@delaware.com', '1 Analyst', FALSE),
                                                                          ('Joanna', 'Moon', 'joanna.moon@delaware.com', '1 Analyst', TRUE),
                                                                          ('Arne', 'Lupo', 'arne.lupo@delaware.com', '1 Analyst', TRUE),
                                                                          ('Britt', 'Stucchi', 'britt.stucchi@delaware.com', '1 Analyst', TRUE),
                                                                          ('Remy', 'Le Goff', 'remy.le goff@delaware.com', '1 Analyst', FALSE),
                                                                          ('Matthew', 'Couturier', 'matthew.couturier@delaware.com', '1 Analyst', FALSE),
                                                                          ('Carlos', 'Heintze', 'carlos.heintze@delaware.com', '1 Analyst', FALSE),
                                                                          ('Lauretta', 'Reising', 'lauretta.reising@delaware.com', '1 Analyst', TRUE),
                                                                          ('Joshua', 'Wouters', 'joshua.wouters@delaware.com', '1 Analyst', TRUE),
                                                                          -- 2 Consultant Technical
                                                                          ('Laura', 'Bousquet', 'laura.bousquet@delaware.com', '2 Consultant Technical', FALSE),
                                                                          ('Carlos', 'Englund', 'carlos.englund@delaware.com', '2 Consultant Technical', TRUE),
                                                                          ('Francisca', 'Alsina', 'francisca.alsina@delaware.com', '2 Consultant Technical', TRUE),
                                                                          ('Sabine', 'Amaral', 'sabine.amaral@delaware.com', '2 Consultant Technical', FALSE),
                                                                          ('Jorge', 'Goncalves', 'jorge.goncalves@delaware.com', '2 Consultant Technical', TRUE),
                                                                          ('Bryan', 'Pierre', 'bryan.pierre@delaware.com', '2 Consultant Technical', FALSE),
                                                                          ('Pierluigi', 'Neto', 'pierluigi.neto@delaware.com', '2 Consultant Technical', TRUE),
                                                                          ('Maurits', 'Davidson', 'maurits.davidson@delaware.com', '2 Consultant Technical', TRUE),
                                                                          ('Cesare', 'Pettersson', 'cesare.pettersson@delaware.com', '2 Consultant Technical', TRUE),
                                                                          ('Bryan', 'Borner', 'bryan.borner@delaware.com', '2 Consultant Technical', FALSE),
                                                                          -- 3 Senior Consultant Technical
                                                                          ('Niccolo', 'Bloch', 'niccolo.bloch@delaware.com', '3 Senior Consultant Technical', FALSE),
                                                                          ('Anna-Karin', 'Moreau', 'anna-karin.moreau@delaware.com', '3 Senior Consultant Technical', TRUE),
                                                                          ('Irma', 'Osuna', 'irma.osuna@delaware.com', '3 Senior Consultant Technical', FALSE),
                                                                          ('Francesca', 'Payne', 'francesca.payne@delaware.com', '3 Senior Consultant Technical', FALSE),
                                                                          ('Sofia', 'Macias', 'sofia.macias@delaware.com', '3 Senior Consultant Technical', TRUE),
                                                                          ('Ilonka', 'Aranda', 'ilonka.aranda@delaware.com', '3 Senior Consultant Technical', TRUE),
                                                                          ('Renato', 'van Berkum', 'renato.van berkum@delaware.com', '3 Senior Consultant Technical', TRUE),
                                                                          ('Gianfrancesco', 'Gregoire', 'gianfrancesco.gregoire@delaware.com', '3 Senior Consultant Technical', FALSE),
                                                                          ('Hilario', 'Toussaint', 'hilario.toussaint@delaware.com', '3 Senior Consultant Technical', FALSE),
                                                                          ('Raffaello', 'Parsons', 'raffaello.parsons@delaware.com', '3 Senior Consultant Technical', FALSE),
                                                                          -- 4 Lead Expert
                                                                          ('Odalys', 'Hentschel', 'odalys.hentschel@delaware.com', '4 Lead Expert', FALSE),
                                                                          ('Jacqueline', 'Baron', 'jacqueline.baron@delaware.com', '4 Lead Expert', TRUE),
                                                                          ('Anders', 'Gonzalez', 'anders.gonzalez@delaware.com', '4 Lead Expert', FALSE),
                                                                          ('Raffaele', 'Avila', 'raffaele.avila@delaware.com', '4 Lead Expert', TRUE),
                                                                          ('Antoine', 'Etzler', 'antoine.etzler@delaware.com', '4 Lead Expert', FALSE),
                                                                          ('Silvia', 'Camps', 'silvia.camps@delaware.com', '4 Lead Expert', TRUE),
                                                                          ('Leticia', 'Sala', 'leticia.sala@delaware.com', '4 Lead Expert', FALSE),
                                                                          ('Jacqueline', 'Campos', 'jacqueline.campos@delaware.com', '4 Lead Expert', FALSE),
                                                                          ('Holly', 'Warmer', 'holly.warmer@delaware.com', '4 Lead Expert', FALSE),
                                                                          ('Berenice', 'Wulff', 'berenice.wulff@delaware.com', '4 Lead Expert', FALSE),
                                                                          -- 5 Manager
                                                                          ('Isaias', 'Glasses', 'isaias.glasses@delaware.com', '5 Manager', TRUE),
                                                                          ('Gundi', 'Rijks', 'gundi.rijks@delaware.com', '5 Manager', TRUE),
                                                                          ('Andre', 'Schmidt', 'andre.schmidt@delaware.com', '5 Manager', FALSE),
                                                                          ('Lucas', 'Comisso', 'lucas.comisso@delaware.com', '5 Manager', TRUE),
                                                                          ('Ferdinando', 'Pazos', 'ferdinando.pazos@delaware.com', '5 Manager', TRUE),
                                                                          ('Maxim', 'Company', 'maxim.company@delaware.com', '5 Manager', TRUE),
                                                                          ('Marijn', 'Geisel', 'marijn.geisel@delaware.com', '5 Manager', TRUE),
                                                                          ('Leonardo', 'James', 'leonardo.james@delaware.com', '5 Manager', FALSE),
                                                                          ('Gunnar', 'Thies', 'gunnar.thies@delaware.com', '5 Manager', TRUE),
                                                                          ('Rafael', 'Majewski', 'rafael.majewski@delaware.com', '5 Manager', TRUE),
                                                                          -- 6 Senior Manager
                                                                          ('Elpidio', 'Dos Santos', 'elpidio.dos santos@delaware.com', '6 Senior Manager', TRUE),
                                                                          ('Sandra', 'Salamanca', 'sandra.salamanca@delaware.com', '6 Senior Manager', FALSE),
                                                                          ('Ann-Charlotte', 'Pinheiro', 'ann-charlotte.pinheiro@delaware.com', '6 Senior Manager', TRUE),
                                                                          ('Lindsey', 'Andersson', 'lindsey.andersson@delaware.com', '6 Senior Manager', FALSE),
                                                                          ('Frank', 'Pereira', 'frank.pereira@delaware.com', '6 Senior Manager', FALSE),
                                                                          ('Monica', 'Cardano', 'monica.cardano@delaware.com', '6 Senior Manager', TRUE),
                                                                          ('Antonio', 'Wieloch', 'antonio.wieloch@delaware.com', '6 Senior Manager', FALSE),
                                                                          ('Inga', 'Vazquez', 'inga.vazquez@delaware.com', '6 Senior Manager', TRUE),
                                                                          ('Sofie', 'Karlsson', 'sofie.karlsson@delaware.com', '6 Senior Manager', FALSE),
                                                                          ('Gundel', 'Pettersson', 'gundel.pettersson@delaware.com', '6 Senior Manager', TRUE),
                                                                          -- 7 DPH Consultant Technical
                                                                          ('Nuno', 'Eriksson', 'nuno.eriksson@delaware.com', '7 DPH Consultant Technical', TRUE),
                                                                          ('Victor Manuel', 'Johansson', 'victor manuel.johansson@delaware.com', '7 DPH Consultant Technical', TRUE),
                                                                          ('Antonio', 'Scheel', 'antonio.scheel@delaware.com', '7 DPH Consultant Technical', TRUE),
                                                                          ('Yasmin', 'Pechel', 'yasmin.pechel@delaware.com', '7 DPH Consultant Technical', FALSE),
                                                                          ('Christophe', 'Leclerc', 'christophe.leclerc@delaware.com', '7 DPH Consultant Technical', FALSE),
                                                                          ('Ulises', 'Gagliano', 'ulises.gagliano@delaware.com', '7 DPH Consultant Technical', TRUE),
                                                                          ('Kristen', 'Eerden', 'kristen.eerden@delaware.com', '7 DPH Consultant Technical', FALSE),
                                                                          ('Fermin', 'Pearson', 'fermin.pearson@delaware.com', '7 DPH Consultant Technical', TRUE),
                                                                          ('Amanda', 'de Roos', 'amanda.de roos@delaware.com', '7 DPH Consultant Technical', FALSE),
                                                                          ('Guillaume', 'Neveu', 'guillaume.neveu@delaware.com', '7 DPH Consultant Technical', TRUE),
                                                                          -- 8 DPH Senior Consultant Technical
                                                                          ('Lucie', 'Boutin', 'lucie.boutin@delaware.com', '8 DPH Senior Consultant Technical', FALSE),
                                                                          ('Daphne', 'Lensen', 'daphne.lensen@delaware.com', '8 DPH Senior Consultant Technical', TRUE),
                                                                          ('Nedda', 'Santos', 'nedda.santos@delaware.com', '8 DPH Senior Consultant Technical', TRUE),
                                                                          ('Lara', 'Pirelli', 'lara.pirelli@delaware.com', '8 DPH Senior Consultant Technical', TRUE),
                                                                          ('Gertrudis', 'Schleich', 'gertrudis.schleich@delaware.com', '8 DPH Senior Consultant Technical', TRUE),
                                                                          ('Luke', 'Bonneau', 'luke.bonneau@delaware.com', '8 DPH Senior Consultant Technical', FALSE),
                                                                          ('Juliana', 'Steinberg', 'juliana.steinberg@delaware.com', '8 DPH Senior Consultant Technical', TRUE),
                                                                          ('Cecile', 'Franzese', 'cecile.franzese@delaware.com', '8 DPH Senior Consultant Technical', FALSE),
                                                                          ('Michela', 'Pujadas', 'michela.pujadas@delaware.com', '8 DPH Senior Consultant Technical', TRUE),
                                                                          ('Matilde', 'Lucas', 'matilde.lucas@delaware.com', '8 DPH Senior Consultant Technical', TRUE),
                                                                          -- 9 DPH Lead Expert/Manager
                                                                          ('Uno', 'White', 'uno.white@delaware.com', '9 DPH Lead Expert/Manager', TRUE),
                                                                          ('Giuliano', 'Hallberg', 'giuliano.hallberg@delaware.com', '9 DPH Lead Expert/Manager', FALSE),
                                                                          ('Darren', 'Menendez', 'darren.menendez@delaware.com', '9 DPH Lead Expert/Manager', TRUE),
                                                                          ('Margarida', 'Persson', 'margarida.persson@delaware.com', '9 DPH Lead Expert/Manager', TRUE),
                                                                          ('Kevin', 'Niemeier', 'kevin.niemeier@delaware.com', '9 DPH Lead Expert/Manager', TRUE),
                                                                          ('Anthony', 'Mangold', 'anthony.mangold@delaware.com', '9 DPH Lead Expert/Manager', FALSE),
                                                                          ('Elisabeth', 'Gustafsson', 'elisabeth.gustafsson@delaware.com', '9 DPH Lead Expert/Manager', FALSE),
                                                                          ('Mesut', 'Loureiro', 'mesut.loureiro@delaware.com', '9 DPH Lead Expert/Manager', FALSE),
                                                                          ('Vincent', 'Poerio', 'vincent.poerio@delaware.com', '9 DPH Lead Expert/Manager', FALSE),
                                                                          ('Molly', 'Correia', 'molly.correia@delaware.com', '9 DPH Lead Expert/Manager', FALSE);




INSERT INTO project_assignments (projectId, employeeId, assignedDate) VALUES
    (1, 1, '2023-01-15'),
    (1, 2, '2023-01-20'),
    (2, 3, '2023-03-06'),
    (2, 4, '2023-03-10'),
    (3, 5, '2023-04-22'),
    (4, 1, '2023-05-16'),
    (4, 3, '2023-05-20'),
    (4, 5, '2023-05-25'),
    (5, 2, '2023-06-02'),
    (5, 4, '2023-06-05');


INSERT INTO roles_rates (role, rate) VALUES
    ('0 Blended FE dev', 200.00),
    ('0 Blended MW dev', 200.00),
    ('0 Blended Overall dev', 200.00),
    ('0 Blended XR dev', 100.00),
    ('1 Analyst', 100.00),
    ('2 Consultant Technical', 150.00),
    ('3 Senior Consultant Technical', 200.00),
    ('4 Lead Expert', 220.00),
    ('5 Manager', 230.00),
    ('6 Senior Manager', 230.00),
    ('7 DPH Consultant Technical', 200.00),
    ('8 DPH Senior Consultant Technical', 200.00),
    ('9 DPH Lead Expert/Manager', 200.00);



# SHOW GRANTS FOR CURRENT_USER();


DELIMITER //

DROP TRIGGER IF EXISTS after_project_assignment_insert;
CREATE TRIGGER after_project_assignment_insert
    AFTER INSERT ON project_assignments
    FOR EACH ROW
BEGIN
    -- Update the employee's availability to FALSE
    UPDATE employees
    SET isAvailable = 0
    WHERE id = NEW.employeeId;
END;
//

DELIMITER ;

DELIMITER //

DROP TRIGGER IF EXISTS after_project_assignment_delete;
CREATE TRIGGER after_project_assignment_delete
    AFTER DELETE ON project_assignments
    FOR EACH ROW
BEGIN
    -- Check if the employee is still assigned to any project
    IF NOT EXISTS (
        SELECT 1
        FROM project_assignments
        WHERE employeeId = OLD.employeeId
    ) THEN
        UPDATE employees
        SET isAvailable = TRUE
        WHERE id = OLD.employeeId;
    END IF;
END;
//

DELIMITER ;



DELIMITER //

DROP TRIGGER IF EXISTS after_project_assignment_update;
CREATE TRIGGER after_project_assignment_update
    AFTER UPDATE ON project_assignments
    FOR EACH ROW
BEGIN
    -- Update availability of the old employee (if no longer assigned to any project)
    IF NOT EXISTS (
        SELECT 1
        FROM project_assignments
        WHERE employeeId = OLD.employeeId
    ) THEN
        UPDATE employees
        SET isAvailable = TRUE
        WHERE id = OLD.employeeId;
    END IF;

    -- Set the new employee to unavailable
    UPDATE employees
    SET isAvailable = FALSE
    WHERE id = NEW.employeeId;
END;
//

DELIMITER ;




# This trigger made it so when an employee is assigned they don't become unavailable
# Not sure if this is the desired behavior

DELIMITER //
DROP TRIGGER IF EXISTS after_project_update;
CREATE TRIGGER after_project_update
    AFTER UPDATE ON projects
    FOR EACH ROW
BEGIN
    -- Check if the project is deactivated (set isActive to FALSE)
    IF OLD.isActive = TRUE AND NEW.isActive = FALSE THEN
        -- Mark all employees assigned to this project as available
    UPDATE employees
    SET isAvailable = TRUE
    WHERE id IN (
        SELECT employeeId
        FROM project_assignments
        WHERE projectId = NEW.id
    );
END IF;
END;
//
DELIMITER ;
