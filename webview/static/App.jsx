function ColumnItem(props) {
	const [deleting, setDeleting] = React.useState(false);

	const deleteColumn = () => {
		$.get('/delete_column', {
			database: props.database,
			table: props.table,
			name: props.item.name
		}, function(data) {
			// props.getTable(props.item.name);
		});
	}

	return (
		<div className="row hover p-1">
			<span className="col fst-italic">{props.item.name}</span>
			<span className="col font-monospace">{props.item.type_}</span>
			<div className="col">
				<span className="btn-group btn-group-sm float-end">
					{deleting && <a onClick={() => deleteColumn()} className="btn text-danger">Delete?</a>}
					<a onClick={() => setDeleting(!deleting)} className="btn text-danger"><i className="bi bi-x-circle"></i></a>
				</span>
			</div>
		</div>
		);
}

function App() {
	const [theme, setTheme] = React.useState(localStorage.getItem('SQLeasy'));
	const [loading, setLoading] = React.useState(false);
	const [deletingDb, setDeletingDb] = React.useState(false);
	const [deletingTable, setDeletingTable] = React.useState(false);
	const [dbs, setDbs] = React.useState([]);
	const [currentDb, setCurrentDb] = React.useState([]);
	const [currentTable, setCurrentTable] = React.useState([]);

	const changeTheme = (theme_) => {
		localStorage.setItem('SQLeasy', theme_);
		document.documentElement.setAttribute('data-theme', theme_);
		setTheme(theme_);
	}

	const showDbs = () => {
		setLoading(true);
		$.get('/show_dbs', function(data) {
			setDbs(data.dbs);
			setLoading(false);
		});
	}

	const createDatabase = (e) => {
		e.preventDefault();
		$.post('/create_database', {
			name: $('#new-db').val()
		}, function(data) {
			$('#new-db').val('');
			showDbs();
			setCurrentDb(data);
		});
	}

	const getDatabase = (name) => {
		setLoading(true);
		$.get('/get_database', {
			name: name
		}, function(data) {
			setCurrentDb(data);
			setLoading(false);
		});
	}

	const deleteDatabase = () => {
		setLoading(true);
		$.get('/delete_database', {
			name: currentDb.name
		}, function(data) {
			showDbs();
			setCurrentDb([]);
			setDeletingDb(false);
			setLoading(false);
		});
	}

	const createTable = (e) => {
		e.preventDefault();
		$.post('/create_table', {
			database: currentDb.name,
			name: $('#new-table').val()
		}, function(data) {
			$('#new-table').val('');
			getDatabase(currentDb.name);
			setCurrentTable(data);
		});
	}

	const getTable = (name) => {
		setLoading(true);
		$.get('/get_table', {
			database: currentDb.name,
			name: name
		}, function(data) {
			setCurrentTable(data);
			setLoading(false);
		});
	}

	const createColumn = (e) => {
		e.preventDefault();
		setLoading(true);
		$.post('/create_column', {
			database: currentDb.name,
			table: currentTable.name,
			name: $('#new-column').val(),
			type_: $('#data-type').val()
		}, function(data) {
			getTable(currentTable.name);
			$('#new-column').val('');
			$('#data-type').val('text');
			setLoading(false);
		});
	}

	const deleteTable = () => {
		setLoading(true);
		$.get('/delete_table', {
			database: currentDb.name,
			name: currentTable.name
		}, function(data) {
			getDatabase(currentDb.name);
			setCurrentTable([]);
			setDeletingTable(false);
			setLoading(false);
		});
	}

	React.useEffect(() => {
		changeTheme(theme);
		showDbs();
	}, []);

	return (
		<div className="p-4">
			<div className="btn-group btn-group-sm">
				<a className="btn text-secondary">{loading ? <span className="spinner-border spinner-border-sm"></span> : <i className="bi bi-database-fill-check"></i>} SQLeasy</a>
				<a data-bs-target="#themes" data-bs-toggle="dropdown" className="btn text-secondary dropdown-toggle text-capitalize"><i className="bi bi-paint-bucket"></i> {theme}</a>
				<div id="themes" className="dropdown-menu text-center">
					{theme !== 'light' && <a onClick={() => changeTheme('light')} className="dropdown-item small text-capitalize">light</a>}
					{theme !== 'dark' && <a onClick={() => changeTheme('dark')} className="dropdown-item small text-capitalize">dark</a>}
				</div>
				<a target="_blank" href="https://github.com/misterrager8/SQLeasy/" className="btn text-secondary"><i className="bi bi-info-circle"></i> About</a>
			</div>
			<div className="row mt-4">
				<div className="col-3">
					<form className="input-group input-group-sm mb-3" onSubmit={(e) => createDatabase(e)}>
						<input required autoComplete="off" className="form-control" placeholder="New Database" id="new-db"/>
						<button type="submit" className="btn btn-outline-success">Create</button>
					</form>
					{dbs.map((x, id) => (
						<div className={'hover px-3 py-1' + (currentDb.name === x ? ' selected' : '')} key={id}>
							<a className="heading" onClick={() => getDatabase(x)}>{x}</a>
						</div>
					))}
				</div>
				<div className="col-3">
					{currentDb.length !== 0 && (
						<div>
							<div className="fs-3 mb-3 heading"><i className="bi bi-chevron-right"></i> {currentDb.name}</div>
							<form className="input-group input-group-sm mb-3" onSubmit={(e) => createTable(e)}>
								<input required autoComplete="off" className="form-control" placeholder="New Table" id="new-table"/>
								<button type="submit" className="btn btn-outline-success">Create</button>
							</form>
							{currentDb.tables.map((x, id) => (
								<div className={'hover px-3 py-1' + (currentTable.name === x ? ' selected' : '')} key={id}>
									<a onClick={() => getTable(x)} className="heading">{x}</a>
								</div>
							))}
							<div className="btn-group btn-group-sm mt-3 w-100">
								<a onClick={() => setDeletingDb(!deletingDb)} className="btn btn-outline-danger"><i className="bi bi-x-circle"></i> Delete Database</a>
								{deletingDb && <a onClick={() => deleteDatabase()} className="btn text-danger">Delete?</a>}
							</div>
						</div>
					)}
				</div>
				<div className="col-6">
					{currentTable.length !== 0 && (
						<div>
							<div className="fs-3 mb-3 heading"><i className="bi bi-chevron-right"></i> {currentTable.name}</div>
							<form className="input-group input-group-sm mb-3" onSubmit={(e) => createColumn(e)}>
								<input required autoComplete="off" className="form-control" placeholder="New Column" id="new-column"/>
								<select className="form-control text-uppercase" id="data-type">
									<option value="text">text</option>
									<option value="int">int</option>
									<option value="datetime">datetime</option>
									<option value="boolean">boolean</option>
								</select>
								<button type="submit" className="btn btn-outline-success">Create</button>
							</form>
							{currentTable.columns.map((x, id) => (
								<ColumnItem getTable={getTable} item={x} database={currentDb.name} table={currentTable.name} key={id}/>
							))}
							<div className="btn-group btn-group-sm mt-3 w-100">
								<a onClick={() => setDeletingTable(!deletingTable)} className="btn btn-outline-danger"><i className="bi bi-x-circle"></i> Delete Table</a>
								{deletingTable && <a onClick={() => deleteTable()} className="btn text-danger">Delete?</a>}
							</div>
						</div>
					)}
				</div>
			</div>
		</div>
		);
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App/>);
