update centralizer_properties set valueRepresentation=concat(floor(valueRepresentation),' 7/8')
where fieldID=2012 and centralizerID>5000 and valueRepresentation like '%.875'

select centralizerID, valueRepresentation, concat( floor(valueRepresentation), ' 3/4')
from centralizer_properties
where fieldID=2009 and centralizerID>5000 and valueRepresentation like '%.75'

update centralizer_properties set valueRepresentation='Rigid'
where fieldID=2049 and centralizerID<5000

update centralizer_properties set valueRepresentation='Bow Spring'
where fieldID=2049 and centralizerID>5000


insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation)
select p.pipeID,(select f.fieldID from fields f where f.abbreviation='USS'),p.nativeUnitID,p.valueRepresentation*0.75
from pipe_properties p where p.fieldID=(select f.fieldID from fields f where f.abbreviation='UTS');


insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation)
select p.pipeID,(select f.fieldID from fields f where f.abbreviation='SYS'),p.nativeUnitID,round(p.valueRepresentation*0.58) 
from pipe_properties p where p.fieldID=(select f.fieldID from fields f where f.abbreviation='TYS');


set @factor = pi()/16/12;
insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation)
select H.pipeID, 2071, 3097, @factor*(pow(H.OD,4)-pow(H.ID,4))/H.OD*H.SYS as TorsionalLimit from
(select Tt.pipeID as pipeID, d as ID, d+2*t as OD, s as SYS from
  (select pipeID, valueRepresentation as t from pipe_properties where fieldID=2047) as Tt
inner join
  (select pipeID, valueRepresentation as d from pipe_properties where fieldID=2031) as Dt
inner join
  (select pipeID, valueRepresentation as s from pipe_properties where fieldID=2070) as St
on Tt.pipeID=Dt.pipeID and St.pipeID=Dt.pipeID) as H