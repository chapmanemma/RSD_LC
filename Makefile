#compiler
#cc = /usr/local/bin/gcc-8
cc = /opt/homebrew/bin/gcc
mpicc = /opt/homebrew/bin/mpicc

#complilation flags

# if FFTW uses openmp:
fftwf = -lfftw3f_omp -lfftw3f
fftwd = -lfftw3_omp -lfftw3
# if FFTW used pthreads:
#fftwf = -lfftw3f_threads -lfftw3f
#fftwd = -lfftw3_threads -lfftw3

omp = -fopenmp -D_OMPTHREAD_
#omp = -Xpreprocessor -fopenmp -D_OMPTHREAD_
gsl = -lgsl -lgslcblas -lm
deb = -g

#flags = -std=c99 -Wall -O3 -march=native $(fftwd) $(fftwf) $(omp) $(gsl) -lm
flags = -std=c99 -Wall -O3 -fcommon $(omp) $(fftwd) $(fftwf) $(gsl) -I . -I/opt/homebrew/include -L/opt/homebrew/lib

auxo = auxiliary.o Input_variables.o 
auxh = auxiliary.h Input_variables.h 

main = RSD_LC RSD_LC_dTb RSD_LC_21cmFAST

# main = get_densityfield.x get_velocityfield.x get_halos.x get_nldensity.x adjust_halos.x \
# 	xalpha.x xc.x epsilonXon.x integratexe.x integrateTempX.x t21.x get_HIIbubbles.x get_SFR.x

# tools = tools/get_halo_deltan.x tools/opdepth.x tools/power3d_f.x tools/power3d_cross.x \
# 	tools/get_dndm_nbins.x tools/adndm.x tools/abias.x tools/power3d.x tools/rz.x tools/vel_grad.x

RSD_LC: $(auxo) RSD_LC_v2.0.o
	$(mpicc) -o RSD_LC RSD_LC_v2.0.o $(auxo) $(flags) #-L/path/to/mpi/lib -I/path/to/mpi/include 

RSD_LC_dTb: $(auxo) RSD_LC_dTb.o
	$(mpicc) -o RSD_LC_dTb RSD_LC_dTb.o $(auxo) $(flags) #-L/path/to/mpi/lib -I/path/to/mpi/include 

RSD_LC_21cmFAST: $(auxo) RSD_LC_21cmFAST.o
	$(mpicc) -o RSD_LC_21cmFAST RSD_LC_21cmFAST.o $(auxo) $(flags) #-L/path/to/mpi/lib -I/path/to/mpi/include 

vel: $(auxo) vel.o
	/opt/homebrew/bin/mpicc -o vel vel.o $(auxo) $(flags) #-L/pat

# %.x: %.o $(auxo)
# 	$(cc) -o $@ $< $(auxo) $(flags)

%: %.o $(auxo)
	$(cc) -o $@ $< $(auxo) $(flags)

%.o: %.c $(auxh)
	${cc} ${flags} -c $< -o $@

.PRECIOUS: %.o

clean:
	rm *.o *.x tools/*.o tools/*.x


