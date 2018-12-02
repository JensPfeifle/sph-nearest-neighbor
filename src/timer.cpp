//----------------------------------------------------------------
/* Timer
Simple timer class using C++11 chrono.
example use:
{
    Timer_t t; // use global typedef for standard timer.
    t.Start(); // start the timer.
    ... do something you want to time ...
    t.End();   // end the timer
    t.CalcDuration; // Calculate and store (inside the Timer class) the interval between start and end.
    cout << "Time in milliseconds: " << t.GetDuration().count() << end; // cout the interval
}
*/
template< typename precision = long double, typename ratio = std::milli >
class Timer final
{
public:
    //---------------- aliases ----------------
    using timeDuration_t = std::chrono::duration<precision, ratio>;
    using timePoint_t = std::chrono::time_point<std::chrono::system_clock, timeDuration_t>;
    using this_type = Timer< precision, ratio >;

    //---------------- special member functions ----------------
    // NOTE: all the default compiler generated member functions will suffice.

    //---------------- member functions ----------------

    //--------------------------------
    /* Start()
        Starts the timer.
    */
    inline void Start()
    {
        m_start = std::chrono::system_clock::now();
    }

    //--------------------------------
    /* End()
        Ends the timer.
    */
    inline void End()
    {
        m_end = std::chrono::system_clock::now();
    }

    //--------------------------------
    /* CalcDuration()
        Calculates the time elapsed (duration)
        in between the previous calls to Start and End().

        NOTE: make sure to have called Start() and End() before calling this function.
        NOTE: Start() and End() can be called in any order.
    */
    void CalcDuration()
    {
        m_duration = std::max( m_start, m_end ) - std::min( m_start, m_end );
    }

    //--------------------------------
    /* GetDuration()
        Returns the calculated duration.

        NOTE: make sure to call CalcDuration() before calling this function.
    */
    timeDuration_t const& GetDuration() const
    {
        return m_duration;
    }

    //--------------------------------
    /* Zero()
        Zeros the internal members, effectively resetting the Timer.
    */
    void Zero()
    {
        m_start = timeDuration_t::zero();
        m_end = m_start;
        m_duration = m_end;
    }

    //--------------------------------
    /* TestLatency( i_count )
        Tests the latency / error of the timer class.

        NOTE: this number is how inaccurate your timings can be.
    */
    static timeDuration_t TestLatency( size_t const i_count = 512 )
    {
        this_type t;
        timeDuration_t tSum = timeDuration_t::duration::zero();
        for( size_t i = 0; i < i_count; ++i )
        {
            t.Start();
            t.End();
            t.CalcDuration();
            tSum += t.GetDuration();
        }
        return tSum / i_count;
    }

private:
    //---------------- private member data ----------------
    timePoint_t     m_start;
    timePoint_t     m_end;
    timeDuration_t  m_duration;
};

using Timer_t = Timer<>;