import uuid

def drop(con, name):
    con.execute(f"drop view if exists {name}")
    con.execute(f"drop table if exists {name}")

class duckframe:
    all_views = {}
    
    def __init__(self, con, rel, name=None):
        self.con = con
        self.rel = rel
        self.persisted_name = None
        self.views = set()
        
    @property
    def columns(self):
        return self.rel.columns
    
    @property
    def dtypes(self):
        return self.rel.dtypes
    
    def select(self, cols):
        return duckframe(self.con, self.rel.project(
            ", ".join(f"{col}" for col in cols)
        ))
    
    @staticmethod
    def unionAll(df1, df2):
        return duckframe(df1.con, df1.rel.union(df2.rel))
    
    def createOrReplaceTempView(self, name):
        drop(self.con, name)
        if self.persisted_name is not None:
            self.con.execute(f'CREATE OR REPLACE VIEW "{name}" AS (SELECT * FROM {self.persisted_name})')
        else:
            self.rel.create_view(name)
            
        self.views.add(name)
        
        frame = self.all_views.get(name)
        if frame is not None and frame is not self:
            frame.views.remove(name)
            
        self.all_views[name] = self
        
    def persist(self):
        if self.persisted_name is not None:
            return self
        
        self.persisted_name = "__" + uuid.uuid4().hex
        self.rel.create(self.persisted_name)
        for name in self.views:
            self.con.execute(f'CREATE OR REPLACE VIEW "{name}" AS (SELECT * FROM {self.persisted_name})')
            
        return self
    
    def unpersist(self):
        if self.persisted_name is None:
            return self
        
        for view in self.views:
            self.rel.create_view(view)
        self.con.execute(f'DROP TABLE "{self.persisted_name}"')
        self.persisted_name = None
        
        return self
    
    def collect(self):
        if self.persisted_name is not None:
            return self.con.query("SELECT * FROM {self.persisted_name}").arrow().to_pandas()
        return self.rel.arrow().to_pandas()

class duckspark:
    def __init__(self, con):
        self.con = con
    def sql(self, query):
        return duckframe(self.con, self.con.query(query))
    class catalog:
        @staticmethod
        def listFunctions():
            return []
