import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Home, 
  Users, 
  BarChart3, 
  Clock, 
  Wifi, 
  WifiOff,
  Play,
  Pause,
  Recycle,
  Info
} from 'lucide-react'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'

const Layout = ({ children }) => {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [systemStatus, setSystemStatus] = useState({
    connected: false,
    monitoring: false
  })
  const location = useLocation()

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    // Fetch system status
    const fetchStatus = async () => {
      try {
        const response = await fetch('/api/dashboard')
        const data = await response.json()
        setSystemStatus({
          connected: data.connected,
          monitoring: data.monitoring
        })
      } catch (error) {
        console.error('Error fetching status:', error)
      }
    }

    fetchStatus()
    const statusInterval = setInterval(fetchStatus, 10000)

    return () => {
      clearInterval(timer)
      clearInterval(statusInterval)
    }
  }, [])

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Empleados', href: '/employees', icon: Users },
    { name: 'Reportes', href: '/reports', icon: BarChart3 },
    { name: 'Horarios', href: '/schedules', icon: Clock },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100">
      {/* Header Corporativo PCSHEK */}
      <motion.header 
        className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-b border-slate-700 shadow-xl h-20 sticky top-0 z-50"
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
          <div className="flex justify-between items-center h-full">
            <div className="flex items-center space-x-6">
              {/* Logo PCSHEK */}
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg">
                  <Recycle className="w-8 h-8 text-white" />
                </div>
                <div className="h-12 border-l border-slate-600 pl-4">
                  <h1 className="text-2xl font-bold text-white">
                    PCSHEK
                  </h1>
                  <div className="flex items-center space-x-2">
                    <Recycle className="w-3 h-3 text-green-400" />
                    <p className="text-sm text-green-400 font-medium">
                      Reciclaje Inteligente
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Separador y título del sistema */}
              <div className="h-12 border-l border-slate-600 pl-4">
                <h2 className="text-lg font-semibold text-slate-200">
                  Sistema de Asistencia
                </h2>
                <p className="text-xs text-slate-400 font-mono">
                  {format(currentTime, "EEEE, d 'de' MMMM - HH:mm:ss", { locale: es })}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Indicador de conexión */}
              <motion.div 
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg backdrop-blur-sm transition-all duration-300 ${
                  systemStatus.connected 
                    ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
                    : 'bg-red-500/20 text-red-300 border border-red-500/30'
                }`}
                animate={{ scale: systemStatus.connected ? 1 : 0.95 }}
                transition={{ duration: 0.3 }}
              >
                {systemStatus.connected ? (
                  <Wifi className="w-4 h-4" />
                ) : (
                  <WifiOff className="w-4 h-4" />
                )}
                <span className="text-sm font-semibold">
                  {systemStatus.connected ? 'Conectado' : 'Desconectado'}
                </span>
              </motion.div>
              
              {/* Indicador de monitoreo */}
              <motion.div 
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg backdrop-blur-sm transition-all duration-300 ${
                  systemStatus.monitoring 
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' 
                    : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                }`}
                animate={{ scale: systemStatus.monitoring ? 1 : 0.95 }}
                transition={{ duration: 0.3 }}
              >
                {systemStatus.monitoring ? (
                  <Play className="w-4 h-4" />
                ) : (
                  <Pause className="w-4 h-4" />
                )}
                <span className="text-sm font-semibold">
                  {systemStatus.monitoring ? 'Activo' : 'Pausado'}
                </span>
              </motion.div>
              
              {/* Botón de info */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-slate-300 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
              >
                <Info className="w-5 h-5" />
              </motion.button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Navigation Tabs */}
      <motion.nav 
        className="bg-white rounded-xl shadow-md p-2 mb-6 mx-4 mt-4 sticky top-24 z-40"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        <div className="flex space-x-2">
          {navigation.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.href
            
            return (
              <motion.div key={item.name} whileHover={{ y: -2 }} whileTap={{ y: 0 }}>
                <Link
                  to={item.href}
                  className={`flex items-center space-x-3 py-3 px-6 rounded-xl transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-semibold">{item.name}</span>
                </Link>
              </motion.div>
            )
          })}
        </div>
      </motion.nav>

      {/* Main Content */}
      <main className="relative px-4 pb-8">
        {children}
      </main>
    </div>
  )
}

export default Layout