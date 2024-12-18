
const Spinner = () => {
    return <div className="spinnerapi"><div className="bounce1"></div><div className="bounce2"></div><div className="bounce3"></div></div>
  }

const Pagination = ({prev, next, onPrevious, onNext}) => {

    const handlePrevious = () => {
        onPrevious();
    }

    const handleNext = () => {
        onNext();
    }

    return (
        <>            
            <div className="row">
                <div className="col">
                    <nav aria-label="Page navigation example">
                        <ul className="pagination justify-content-end">
                            {
                                prev ?
                                <li className="page-item">
                                    <button className="page-link" onClick={handlePrevious}>Anterior </button>
                                </li>
                                :
                                <li className="page-item disabled">
                                    <a className="page-link">Anterior</a>
                                </li>
                          
                            }
                            {/* <li className="page-item active"><a className="page-link" href="#">1</a></li>
                            <li className="page-item"><a className="page-link" href="#">2</a></li> */}
                            {
                                next ?
                                <li className="page-item">
                                    <button className="page-link" onClick={handleNext}>Siguiente</button>
                                </li>
                                :
                                <li className="page-item disabled">
                                    <a className="page-link">Siguiente</a>
                                </li>
                            }
                        </ul>
                    </nav>
                </div>
            </div>
        </>
    )
}

const useFormulario = (initialState = {}) => {
    const [inputs, setInputs] = React.useState(initialState);

    const handleChange = (e) => {
        const { name, value, checked, type } = e.target;

        setInputs((old) => ({
            ...old,
            [name]: type === "checkbox" ? checked : value,
        }));
    };

    const reset = () => {
        setInputs(initialState);
    };

    return [inputs, handleChange, reset];
}

const Formulario = ({setTerminoBusqueda}) => {

    const [inputs, handleChange, reset] = useFormulario({
        nombre: '',
    })

    const {nombre} = inputs

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!nombre.trim()) {
            return Swal.fire({
                title: '¡Escriba algo en el buscador!',
                text: '',
                icon: 'info',
                showConfirmButton: false,
				timer: 3000,
            });
        }

        setTerminoBusqueda(nombre.trim())
        reset();
    }

    return (
        <div className="row justify-content-end">
            <div className="col-md-4">
                <form onSubmit={handleSubmit} className="mb-3 text-end">
                    <div className="input-group">                
                        <input type="text" name="nombre" value={nombre} onChange={handleChange} placeholder="Buscar..." className="form-control"/>
                        <button type="submit" className="btn btn-outline-primary">Buscar</button>
                        <button className="btn btn-outline-primary" type="button" onClick={() => setTerminoBusqueda("")}>Limpiar</button>
                    </div>
                </form>
            </div>
        </div>
    )
}

const GetUsers = () => {
    const [users, setUsers] = React.useState([]);

    const [info, setInfo] = React.useState({});

    const [isLoading, setIsLoading] = React.useState(false);

    const [terminoBusqueda, setTerminoBusqueda] = React.useState("");

    const urlSearch = '/api_users/usuarios/?search='

    const [errorMessage, setErrorMessage] = React.useState("");

    const fetchLinks = (url, nombre) => {
        setIsLoading(true);
        fetch(url + nombre)
        .then(response => response.json())
        .then(data => {
            if(data.results.length > 0) {
                setUsers(data.results);
                setInfo(data);
                setIsLoading(false);
            }else{
                setIsLoading(false);
                return Swal.fire({
                    title: '¡Término de búsqueda no encontrado!',
                    text: '',
                    icon: 'error',
                    showConfirmButton: false,
					timer: 3000,
                });
            }
        })
        .catch(() => {
            setErrorMessage("Unable to fetch logs list");
            setIsLoading(false);
        });
    };

    const fetchLinksPaginate = (url) => {
        setIsLoading(true);
        fetch(url)
        .then(response => response.json())
        .then(data => {
            setUsers(data.results);
            setInfo(data);
            setIsLoading(false);
        })
        .catch(() => {
            setErrorMessage("Unable to fetch logs list");
            setIsLoading(false);
        });
    };

    const onPrevious = () => {
        fetchLinksPaginate(info.previous);
    }

    const onNext = () => {
        fetchLinksPaginate(info.next);
    }

    React.useEffect(() => {
        fetchLinks(urlSearch, terminoBusqueda);
    }, [terminoBusqueda])

    return (
        <>
            <Formulario setTerminoBusqueda={setTerminoBusqueda}/>
            <Listusers listusers={users} spinner={isLoading} count={info.count} errormsg={errorMessage} terminoBusqueda={terminoBusqueda} />
            <Pagination prev={info.previous} next={info.next} onPrevious={onPrevious} onNext={onNext} />
        </>
    )
}


const root = ReactDOM.createRoot(document.getElementById('usuarioslist'));
root.render(
    <React.StrictMode>
      <GetUsers />
    </React.StrictMode>
  );
