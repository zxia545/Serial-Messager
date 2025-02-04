// fastserial.c
#include <Python.h>
#include <unistd.h>
#include <sys/select.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

/*
 * comms_read(fd, num_bytes, timeout_ms)
 *
 * Reads up to num_bytes from the file descriptor fd.
 *
 * Parameters:
 *   fd         - an integer file descriptor (from pySerial.fileno())
 *   num_bytes  - number of bytes to read
 *   timeout_ms - timeout in milliseconds; if 0, block indefinitely
 *
 * Returns:
 *   A Python bytes object containing the bytes read.
 *   If timeout_ms > 0 and the timeout expires before num_bytes are read,
 *   the function returns a bytes object with the bytes accumulated so far.
 */
static PyObject* comms_read(PyObject* self, PyObject* args) {
    int fd;
    int num_bytes;
    int timeout_ms;

    if (!PyArg_ParseTuple(args, "iii", &fd, &num_bytes, &timeout_ms)) {
        return NULL;
    }
    if (num_bytes <= 0) {
        PyErr_SetString(PyExc_ValueError, "num_bytes must be positive");
        return NULL;
    }

    char *buffer = (char *)malloc(num_bytes);
    if (buffer == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    size_t total_read = 0;
    struct timeval start, current;
    gettimeofday(&start, NULL);

    while (total_read < (size_t)num_bytes) {
        long elapsed_ms = 0;
        if (timeout_ms > 0) {
            gettimeofday(&current, NULL);
            elapsed_ms = (current.tv_sec - start.tv_sec) * 1000 +
                         (current.tv_usec - start.tv_usec) / 1000;
            if (elapsed_ms >= timeout_ms)
                break;  // Timeout reached
        }
        
        // Calculate remaining time for select (if timeout_ms > 0)
        struct timeval tv;
        if (timeout_ms > 0) {
            long remaining_ms = timeout_ms - elapsed_ms;
            tv.tv_sec = remaining_ms / 1000;
            tv.tv_usec = (remaining_ms % 1000) * 1000;
        }

        fd_set read_fds;
        FD_ZERO(&read_fds);
        FD_SET(fd, &read_fds);

        int ret = select(fd + 1, &read_fds, NULL, NULL, (timeout_ms > 0) ? &tv : NULL);
        if (ret < 0) {
            free(buffer);
            PyErr_SetFromErrno(PyExc_IOError);
            return NULL;
        }
        if (ret == 0) {
            // Timeout for this iteration, break out to return what we have.
            break;
        }
        
        ssize_t r = read(fd, buffer + total_read, num_bytes - total_read);
        if (r < 0) {
            free(buffer);
            PyErr_SetFromErrno(PyExc_IOError);
            return NULL;
        }
        total_read += r;
    }
    
    // Build a Python bytes object from the buffer.
    PyObject* result = Py_BuildValue("y#", buffer, total_read);
    free(buffer);
    return result;
}

static PyMethodDef FastSerialMethods[] = {
    {"comms_read", comms_read, METH_VARARGS,
     "Read a specified number of bytes from the serial file descriptor.\n\n"
     "Parameters:\n"
     "  fd (int): File descriptor for the serial port\n"
     "  num_bytes (int): Number of bytes to read\n"
     "  timeout_ms (int): Timeout in milliseconds (0 to block indefinitely)\n\n"
     "Returns:\n"
     "  bytes: The bytes read (may be fewer than num_bytes if timeout occurs)."},
    {NULL, NULL, 0, NULL}  // Sentinel
};

static struct PyModuleDef fastserialmodule = {
    PyModuleDef_HEAD_INIT,
    "fastserial",       // Module name
    "Module for fast serial I/O using C", // Module documentation
    -1,                 // Per-interpreter state of the module, -1 if state is global.
    FastSerialMethods
};

PyMODINIT_FUNC PyInit_fastserial(void) {
    return PyModule_Create(&fastserialmodule);
}
